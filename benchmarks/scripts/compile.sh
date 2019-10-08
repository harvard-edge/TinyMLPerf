export TOOLCHAIN_DIR=/usr/local/gcc-arm-none-eabi-4/bin; 
export PATH=$TOOLCHAIN_DIR:$PATH; 

# Gitpath is weird because mbed prog code is its own dir. Need 1 level up
gitpath=`echo \`git rev-parse --show-toplevel\`"/../"`

echo "\
mbed compile \
-m auto \
-t GCC_ARM \
-DMBED_ALL_STATS_ENABLED=1 \
--profile ${gitpath}/benchmarks/misc/mbed_include_files/release.json"

mbed compile \
-m auto \
-t GCC_ARM \
-DMBED_ALL_STATS_ENABLED=1 
#--profile ${gitpath}/benchmarks/misc/mbed_include_files/release.json

