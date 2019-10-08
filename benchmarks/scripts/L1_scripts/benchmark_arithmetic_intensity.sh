#!/bin/bash

generate_dir="arithmetic_intensity_tasks"
compile_dir="arithmetic_intensity_compile"
outpath=$1

rm -rf ${generate_dir}
mkdir -p ${generate_dir}
rm -rf ${outpath}
mkdir -p ${outpath}
rm -rf ${compile_dir}
mkdir -p ${compile_dir}

pushd ${compile_dir}
mbed new .
popd

# Generate directories for 10, 100, 1000, 10000, 100000 byte read/write
python3 benchmarks/src/generate.py --tier L1 --task ArithmeticIntensityTask --output-path ${generate_dir} --nfloats "[128, 65536]" --arith_intens "[.5, 1, 2, 4, 8, 16, 32, 64]"

for i in 128 65536; do
   for j in 0.5 1 2 4 8 16 32 64; do
        # Compile and run
        dirpath="${generate_dir}/ArithmeticIntensityTask/nfloats=${i}_arith_intens=${j}/"
        echo "python3 benchmarks/scripts/compile_programs.py --target ${dirpath} --mbed-program-dir ${compile_dir}"
        python3 benchmarks/scripts/compile_programs.py --target ${dirpath} --mbed-program-dir ${compile_dir}
        python3 benchmarks/scripts/run_on_mcu.py --target ${dirpath} --timelimit 30 --output_path ${dirpath}/run_output
        tail -n 1 ${dirpath}/run_output > ${dirpath}/stats.json
        cp ${dirpath}/stats.json ${outpath}/ArithmeticIntensityTask_nfloats=${i}_arith_intens=${j}.json
    done
done