#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

python3 ${DIR}/deep_mlp.py $1 $2 2>/dev/null
utensor-cli convert ${DIR}/mnist_model/deep_mlp.pb --output-nodes=y_pred 2>/dev/null

echo "cp -f ${DIR}/models/* src/"
echo "cp -f ${DIR}/mnist_model/deep_mlp.pb src/"

cp -f ${DIR}/models/* src/
cp -f ${DIR}/mnist_model/deep_mlp.pb src/

# Cleanup
rm -rf ${DIR}/models
rm -rf ${DIR}/mnist_model
rm -rf ${DIR}/mnist_data
rm -rf ${DIR}/constants
rm -rf ${DIR}/chkps