#!/bin/bash

generate_dir="mnist_fc_sparsity_tasks"
compile_dir="mnist_fc_sparsity_compile"
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

sp=( 0 50 80 90 95 98 )

#python3 benchmarks/src/generate.py --tier L3 --task MnistFCSparsity --output-path ${generate_dir} --sparsity "[0,50,80,90,95,98]"

for i in "${sp[@]}"; do
    # Compile and run
    dirpath="${generate_dir}/MnistFCSparsity/sparsity=${i}/"
    echo "python3 benchmarks/scripts/compile_programs.py --target ${dirpath} --mbed-program-dir ${compile_dir}"
    python3 benchmarks/scripts/compile_programs.py --target ${dirpath} --mbed-program-dir ${compile_dir}
    python3 benchmarks/scripts/run_on_mcu.py --target ${dirpath} --timelimit 30 --output_path ${dirpath}/run_output
    tail -n 1 ${dirpath}/run_output > ${dirpath}/stats.json
    cp ${dirpath}/stats.json ${outpath}/MnistFCSparsityTask_sparsity=${i}.json
done
