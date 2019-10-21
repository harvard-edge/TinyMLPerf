#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

echo "Mnist FC train_and_generate.sh running deep_mlp.py"
python3 ${DIR}/deep_mlp.py $1 $2  2>/dev/null

echo "Mnist FC train_and_generate.sh utensor-cli convert"
# Once for extracting the final graph transform, again for generating cpp files
utensor-cli convert ${DIR}/mnist_model/deep_mlp.pb --output-nodes=y_pred --save-graph --transform-methods dropout,quantize,biasAdd,remove_id_op,refcnt 2>/dev/null
mv quant_deep_mlp.pkl quant_deep_mlp_target.pkl
utensor-cli convert ${DIR}/mnist_model/deep_mlp.pb --output-nodes=y_pred --save-graph 2>/dev/null

echo "cp -f ${DIR}/models/* ${DIR}/../src/"
echo "cp -f ${DIR}/mnist_model/deep_mlp.pb ${DIR}/../src/"
echo "cp -f ${DIR}/mnist_model/deep_mlp_final.pb ${DIR}/../src/"

cp -f ${DIR}/models/* ${DIR}/../src/
cp -f ${DIR}/mnist_model/deep_mlp.pb ${DIR}/../src/
cp -f ${DIR}/mnist_model/deep_mlp_final.pb ${DIR}/../src/

# Cleanup
rm -rf ${DIR}/models
rm -rf ${DIR}/mnist_model
rm -rf ${DIR}/mnist_data
rm -rf ${DIR}/constants
rm -rf ${DIR}/chkps