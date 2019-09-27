import sys
import importlib
import glob
import os
import argparse

parser = argparse.ArgumentParser()

tier_directories = ['L1','L2','L3']

parser.add_argument('--tier', default=None, choices=tier_directories)
parser.add_argument('--task', default=None, type=str)
parser.add_argument('--output_path', default=None, type=str)

if __name__ == "__main__":
    args = parser.parse_args()
    assert(args.tier != None)
    assert(args.task != None)
    assert(args.output_path != None)

    # Load all the tasks from L1/L2/L3 directories
    self_full_path = os.path.dirname(os.path.abspath(__file__))
    tiers_tasks_dict = {}
    for d in tier_directories:
        tier_directory_path = "/".join([self_full_path, d])
        assert(os.path.exists(tier_directory_path))
        for module_path in glob.glob(tier_directory_path + "/*.py"):
            module_name = module_path.split("/")[-1].replace(".py", "")
            print("Loading: module %s with path %s" % 
                  (module_name, module_path))
            spec = importlib.util.spec_from_file_location(module_name,
                                                          module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            

    # Make the output directory
    if not os.path.exists(args.output_path):
        os.makedirs(args.output_path)

        
