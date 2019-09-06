REDIS_CLI=redis-cli

echo "SET MODEL"
$REDIS_CLI -x AI.MODELSET sklearn_logistic ONNX CPU < ../models/sklearn/logistic_regression/logistic.onnx

echo "SET TENSORS"
$REDIS_CLI AI.TENSORSET a FLOAT 1 4

echo "GET TENSORS"
$REDIS_CLI AI.TENSORGET a META

echo "RUN MODEL"
$REDIS_CLI AI.MODELRUN sklearn_logistic INPUTS a OUTPUTS b c

echo "GET TENSOR META"
$REDIS_CLI AI.TENSORGET b META

echo "GET TENSOR VALUES"
$REDIS_CLI AI.TENSORGET b VALUES

echo "GET TENSOR VALUES"
$REDIS_CLI AI.TENSORGET c VALUES  # Wrong value

echo "GET TENSOR BLOB"
$REDIS_CLI AI.TENSORGET b BLOB

$REDIS_CLI DEL sklearn_logistic a b