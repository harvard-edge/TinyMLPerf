#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

echo "Mnist FC train_and_generate.sh running deep_mlp.py"
python3 deep_mlp.py $1 $2 $3 2>/dev/null
python3 generate_code.py > baseline.c

# Cleanup
rm -rf ${DIR}/models 
rm -rf ${DIR}/mnist_model
rm -rf ${DIR}/mnist_data
rm -rf ${DIR}/constants
rm -rf ${DIR}/chkps