#!/bin/bash

python3 deep_mlp.py 
utensor-cli convert mnist_model/deep_mlp.pb --output-nodes=y_pred