import sys
import itertools
import inspect
import importlib
import glob
import os
import argparse
from task import Task

parser = argparse.ArgumentParser()

filter_modules = ["__init__"]
tier_directories = ['L1','L2','L3']

parser.add_argument('--tier', default=None, choices=tier_directories)
parser.add_argument('--task', default=None, type=str)
parser.add_argument('--output_path', default=None, type=str)

def load_tiers_and_tasks():
    # Load all the tasks from L1/L2/L3 directories
    self_full_path = os.path.dirname(os.path.abspath(__file__))
    tiers_tasks_dict = {}
    task_names = set()
    for d in tier_directories:
        tiers_tasks_dict[d] = {}
        tier_directory_path = "/".join([self_full_path, d])
        assert(os.path.exists(tier_directory_path))
        for module_path in glob.glob(tier_directory_path + "/*.py"):
            module_name = module_path.split("/")[-1].replace(".py", "")
            if module_name in filter_modules:
                continue
            print("Loading module: %s with path %s" % 
                  (module_name, module_path))
            
            # Load module
            spec = importlib.util.spec_from_file_location(module_name,
                                                          module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Load class
            clsmembers = inspect.getmembers(module,
                                            inspect.isclass)
            clsmembers = [x for x in clsmembers if issubclass(x[1], Task) 
                          and x[1] is not Task]
            
            for cls_name, cls in clsmembers:
                task_name = cls().task_name()
                assert(task_name not in task_names)
                task_names.add(task_name)
                tiers_tasks_dict[d][task_name] = cls
                print("Loaded %s/%s" % (d, task_name))
    return task_names, tiers_tasks_dict

def materialize_argument_ranges(raw_arg_list):
    argwords = raw_arg_list[0:len(raw_arg_list):2]
    ranges = raw_arg_list[1:len(raw_arg_list):2]
    ranges_materialized = [list(eval(x)) for x in ranges]
    return argwords, ranges_materialized

if __name__ == "__main__":
    args, unknown_args = parser.parse_known_args()
    assert(args.tier != None)
    assert(args.task != None)
    assert(args.output_path != None)

    # Make the output directory
    if not os.path.exists(args.output_path):
        os.makedirs(args.output_path)

    # Run
    task_names, tiers_tasks_dict = load_tiers_and_tasks()
    assert(args.task in task_names)
    
    # Cross product over task argument ranges
    task_argwords, task_values = materialize_argument_ranges(unknown_args)
    for paramset in itertools.product(*task_values):
        assert(len(task_argwords) == len(paramset))
        arg_list = [str(val) for pair in zip(task_argwords, paramset) for val in pair]
        task = tiers_tasks_dict[args.tier][args.task]()
        task_args = task.get_parser().parse_args(arg_list)
        task.generate_task(args.output_path, task_args)
