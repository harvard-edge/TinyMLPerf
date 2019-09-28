#!/bin/sh

mbed new mcu_program
cd mcu_program

mbed add http://www.github.com/uTensor/uTensor

# Need to replace the version of uTensor release.json
# because there is a bug where we need gnu tools to
# compile neural networks

cd ..
cp templates/release.json mcu_program/uTensor/extras/build_profile/
cp templates/compile.sh mcu_program/

