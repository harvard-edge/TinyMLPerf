export TOOLCHAIN_DIR=/usr/local/gcc-arm-none-eabi-6/bin; 
export PATH=$TOOLCHAIN_DIR:$PATH; 
mbed compile \
-m auto \
-t GCC_ARM \
--profile uTensor/extras/build_profile/release.json
