#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

#python3 ${DIR}/deep_mlp.py $1 $2  2>/dev/null
#utensor-cli convert ${DIR}/mnist_model/deep_mlp.pb --output-nodes=y_pred --save-graph --transform-methods dropout,quantize,biasAdd,remove_id_op,refcnt 2>/dev/null
python3 ${DIR}/gather_channeled_data.py quant_deep_mlp_target.pkl  2>/dev/null

# Cleanup
rm -rf ${DIR}/models
rm -rf ${DIR}/mnist_model
rm -rf ${DIR}/mnist_data
rm -rf ${DIR}/constants
rm -rf ${DIR}/chkps
