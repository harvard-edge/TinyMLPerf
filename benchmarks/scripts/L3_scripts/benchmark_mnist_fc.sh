#!/bin/bash

generate_dir="mnist_fc_tasks"
compile_dir="mnist_fc_compile"
outpath=$1

#rm -rf ${generate_dir}
#mkdir -p ${generate_dir}
rm -rf ${outpath}
mkdir -p ${outpath}
rm -rf ${compile_dir}
mkdir -p ${compile_dir}

pushd ${compile_dir}
mbed new .
cp ../artifacts/release.json .
popd

h1_size=( 8 16 32 64 128 256 512 1024 )
h2_size=( 8 16 32 64 128 256 512 1024 )

# Generate directories for 10, 100, 1000, 10000, 100000 byte read/write
#python3 benchmarks/src/generate.py --tier L3 --task MnistFC --output-path ${generate_dir} --h1_size "[8,16,32,64,128,256,512,1024]" --h2_size "[8,16,32,64,128,256,512,1024]"

for i in "${h1_size[@]}"; do
    for j in "${h2_size[@]}"; do
        # Compile and run
        dirpath="${generate_dir}/MnistFC/h1_size=${i}_h2_size=${j}/"
        echo "python3 benchmarks/scripts/compile_programs.py --target ${dirpath} --mbed-program-dir ${compile_dir}"
        python3 benchmarks/scripts/compile_programs.py --target ${dirpath} --mbed-program-dir ${compile_dir}
        python3 benchmarks/scripts/run_on_mcu.py --target ${dirpath} --timelimit 30 --output_path ${dirpath}/run_output
        tail -n 1 ${dirpath}/run_output > ${dirpath}/stats.json
        cp ${dirpath}/stats.json ${outpath}/MnistFCTask_h1_size=${i}_h2_size=${j}.json
    done
done
