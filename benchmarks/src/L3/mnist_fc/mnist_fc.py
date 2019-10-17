import sys
import subprocess
import glob
import os
import re
import argparse
from task import Task
from shutil import copyfile, rmtree
from distutils.dir_util import copy_tree

filepath =  os.path.dirname(os.path.abspath(__file__))
template_path = filepath + "/" + "template.c"

class MnistFC(Task):
    def __init__(self):
        self.parser = argparse.ArgumentParser()

        self.parser.add_argument("--h1_size", default=None, type=int)
        self.parser.add_argument("--h2_size", default=None, type=int)

    def generate_task(self, output_path, args):                
        assert(args.h1_size is not None)
        assert(args.h2_size is not None)
        
        # Copy source files over
        source_files = ["%s/src" % filepath, "%s/train" % filepath]
        for src in source_files:

            src_name = src.split("/")[-1]
            if os.path.isdir(src):
                copy_tree("%s" % src, output_path+"/"+src_name)
            else:
                copyfile(src, output_path + "/" + src_name) 

        # Run the script to generate hpp
        cmd = "bash train_and_generate.sh %d %d" % (args.h1_size, args.h2_size)
        commands = ["cd %s/train && %s" % (output_path, cmd)]
        process = subprocess.Popen(commands, stdout=subprocess.PIPE, shell=True)
        out, err = process.communicate()

        print(out.decode('utf-8'))

        # Remove the train directory
        rmtree("%s/train" % output_path)

        # Super hacky, but replace the src/main.cpp file with template
        # and insert args + results
    
    def task_name(self):
        return "MnistFC"

    def get_parser(self):
        return self.parser
        
