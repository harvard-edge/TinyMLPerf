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
from distutils.dir_util import copy_tree

parser = argparse.ArgumentParser()

parser.add_argument("--mbed-program-dir", default="mbed_prog")
parser.add_argument("--target", default=None, required=True)
args = parser.parse_args()

ROOT_MBED_PROGRAM_DIR = Path.cwd() / args.mbed_program_dir

if not ROOT_MBED_PROGRAM_DIR.is_dir():
    os.makedirs(ROOT_MBED_PROGRAM_DIR)

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

def copy_tree_timestamp(src, dst):
    copy_tree(src, dst)
    for dirpath, _, filenames in os.walk(dst):
        os.utime(dirpath, None)
        for file in filenames:
            os.utime(os.path.join(dirpath, file), None)

def process_model_folder(model_folder):
    """Process model folders. Checks whether or not there is a .cpp, .hpp, and
    weights file. If there is, then we copy these files to our MBED program,
    and attempt compiling. If we get a successful result, then we copy the
    .bin file corresponding program back into our models file so we can flash
    the MCU with the file later.
    
    @param model_folder: Path object corresponding to the model .pb folder.
    """
    mcu_name = util.get_mcu()
    files = list(model_folder.glob("*"))
    if not files:
        print("There were no files found, skipping directory {}".format(model_folder))
        return
    else:
        print("Copying files", files)

    # Copy all files over
    print("Copying files to our MBED program directory.")
    for source_file in files:        
        if os.path.isdir(str(source_file)):
            dir_name = str(source_file).split("/")[-1]
            shutil.rmtree(str(ROOT_MBED_PROGRAM_DIR) + "/" + dir_name, ignore_errors=True)
            copy_tree_timestamp(str(source_file), str(ROOT_MBED_PROGRAM_DIR) + "/" + dir_name)
        else:
            src_name = str(source_file).split("/")[-1]
            if os.path.exists(str(ROOT_MBED_PROGRAM_DIR) + "/" + src_name):
                os.remove(str(ROOT_MBED_PROGRAM_DIR) + "/" + src_name)
            shutil.copy(source_file, ROOT_MBED_PROGRAM_DIR)

    # Copy over depended files (standard files that are needed and included for 
    # all tasks)
    copy_over_depended_files()
    
    # Now call the compilation.        
    run(['sh', str(project_base_dir) + '/benchmarks/scripts/compile.sh'], cwd=str(ROOT_MBED_PROGRAM_DIR))
    compiled_binary_files = list((ROOT_MBED_PROGRAM_DIR / 'BUILD/').glob("*/*RELEASE/*.bin"))
    if not compiled_binary_files:
        print("Couldn't find the compiled binary")
        return

    compiled_binary_file = compiled_binary_files[0]

    # If this was successful, copy the file back to our model directory.
    compiled_path = model_folder / '{}_prog.bin'.format(mcu_name)
    shutil.copy(str(compiled_binary_file), str(compiled_path))

    print("Writing compiled binary to: %s" % str(compiled_path))
    

def main():
    process_model_folder(Path.cwd() / args.target)

if __name__ == '__main__':
    main()
