from tensorflow.python.framework.convert_to_constants import convert_variables_to_constants_v2
from tensorflow.python.compiler.tensorrt import trt_convert as trt
import logging
import sys
import tensorflow_hub as hub
import tensorflow as tf
import os

#  restricting execution to a specific device or set of devices for debugging and testing
os.environ['CUDA_VISIBLE_DEVICES'] = '0'
# on aws dl ami source activate tensorflow_p36


compiled_version = trt.wrap_py_utils.get_linked_tensorrt_version()
loaded_version = trt.wrap_py_utils.get_loaded_tensorrt_version()
print("$$$$$$$$$$$$$$$$$$$$$$$$ Linked TensorRT version: %s" %
      str(compiled_version))
print("$$$$$$$$$$$$$$$$$$$$$$$$ Loaded TensorRT version: %s" %
      str(loaded_version))

trt._check_trt_version_compatibility()

logging.getLogger("tensorflow").setLevel(logging.ERROR)

tf_trt_model_path = '../../models/tensorflow/mobilenet/mobilenet_v1_100_224_gpu_NxHxWxC_fp16_trt.pb'

gpu_available = tf.test.is_gpu_available(
    cuda_only=True, min_cuda_compute_capability=None
)

print("TensorFlow version: ", tf.__version__)
if gpu_available is False:
    print("No CUDA GPUs found. Exiting...")
    sys.exit(1)

full_model = tf.keras.Sequential([
    hub.KerasLayer(
        "https://tfhub.dev/google/imagenet/mobilenet_v1_100_224/classification/4")
])
full_model.build([None, 224, 224, 3])  # Batch input shape.

batch_size = 1
height, width = 224, 224
input_var = 'input'
output_var = 'MobilenetV1/Predictions/Reshape_1'

conversion_params = trt.DEFAULT_TRT_CONVERSION_PARAMS._replace(
    precision_mode=trt.TrtPrecisionMode.FP16)

frozen_func = convert_variables_to_constants_v2(full_model)
frozen_func.graph.as_graph_def()

print("Optimizing the model with TensorRT")

converter = trt.TrtGraphConverterV2(
    input_graph_def=frozen_func,
    conversion_params=conversion_params)

frozen_optimized = converter.convert()
directory = os.path.dirname(tf_trt_model_path)
file = os.path.basename(tf_trt_model_path)
tf.io.write_graph(graph_or_graph_def=frozen_func.graph,
                  logdir=".",
                  name=file,
                  as_text=False)
