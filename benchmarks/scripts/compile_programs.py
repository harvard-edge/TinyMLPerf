"""Compiles the programs for our connected MCU and stores them inside the same
folders used for training that hold the model .pb files as well as the converted
C++ files."""
from subprocess import run
from distutils.dir_util import copy_tree
import numpy as np
import time
import os
from pathlib import Path
import shutil
import util
import sys
import argparse
import glob
import git

parser = argparse.ArgumentParser()

parser.add_argument("--mbed-program-dir", default="mbed_prog")
parser.add_argument("--target", default=None)
args = parser.parse_args()

ROOT_MBED_PROGRAM_DIR = Path.cwd() / args.mbed_program_dir

if not os.path.exists(ROOT_MBED_PROGRAM_DIR):
    os.makedirs(ROOT_MBED_PROGRAM_DIR);

def get_git_root(path):
    git_repo = git.Repo(path, search_parent_directories=True)
    git_root = git_repo.git.rev_parse("--show-toplevel")
    return git_root

project_base_dir = get_git_root(os.path.dirname(os.path.abspath(__file__))) 

def copy_over_depended_files():
    print("Copying over depended files to mbed program...")
    MBED_PROGRAM_DIR_INCLUDE_FILES = get_git_root(project_base_dir) + "/benchmarks/misc/mbed_include_files/"
    if not os.path.exists(MBED_PROGRAM_DIR_INCLUDE_FILES):
        print("Error: Mbed program include files directory does not exist (%s)" % MBED_PROGRAM_DIR_INCLUDE_FILES)
    copy_tree(MBED_PROGRAM_DIR_INCLUDE_FILES, str(ROOT_MBED_PROGRAM_DIR))

def process_model_folder(model_folder):
    """Process model folders. Checks whether or not there is a .cpp, .hpp, and
    weights file. If there is, then we copy these files to our MBED program,
    and attempt compiling. If we get a successful result, then we copy the
    .bin file corresponding program back into our models file so we can flash
    the MCU with the file later.
    
    @param model_folder: Path object corresponding to the model .pb folder.
    """
    mcu_name = util.get_mcu()
    cpp_files = list(model_folder.glob("*.[h|c]pp"))
    if not cpp_files:
        print(f"There were no c++ files found, skipping directory {model_folder}")
        return

    # If we found C++ files, make sure that there are only 3, and we can copy
    # this to our mbed program, and attempt to compile.    
    print("Copying files to our MBED program directory.")
    for cpp_source_file in cpp_files:
        shutil.copy(cpp_source_file, ROOT_MBED_PROGRAM_DIR)

    # Copy over depended files (standard files that are needed and included for 
    # all tasks)
    copy_over_depended_files()
    
    # Now call the compilation.        
    run(['sh', project_base_dir + '/benchmarks/scripts/compile.sh'], cwd=ROOT_MBED_PROGRAM_DIR)
    compiled_binary_files = list((ROOT_MBED_PROGRAM_DIR / 'BUILD').glob("*/*/*.bin"))
    if not compiled_binary_files:
        print("Couldn't find the compiled binary")
        return
    compiled_binary_file = compiled_binary_files[0]

    # If this was successful, copy the file back to our model directory.
    compiled_path = model_folder / '{}_prog.bin'.format(mcu_name)
    shutil.copy(compiled_binary_file, compiled_path)
    

def main():
    process_model_folder(Path.cwd() / args.target)

if __name__ == '__main__':
    main()
