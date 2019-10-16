#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

python3 ${DIR}/deep_mlp.py $1 $2
utensor-cli convert ${DIR}/mnist_model/deep_mlp.pb --output-nodes=y_pred

cp -f models/* src/

# Cleanup
rm -rf models
rm -rf mnist_model
rm -rf mnist_data
rm -rf constants
rm -rf chkps