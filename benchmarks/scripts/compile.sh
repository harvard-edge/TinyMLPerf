export TOOLCHAIN_DIR=/usr/local/gcc-arm-none-eabi-4/bin; 
export PATH=$TOOLCHAIN_DIR:$PATH; 
mbed compile \
-m auto \
-t GCC_ARM \
--profile release.json
