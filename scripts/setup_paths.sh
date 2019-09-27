base_dir=`git rev-parse --show-toplevel`
echo $base_dir
export PYTHONPATH="${PYTHONPATH}:$base_dir/benchmarks/src"