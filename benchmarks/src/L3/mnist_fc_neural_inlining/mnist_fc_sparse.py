import sys
import json
import subprocess
import glob
import os
import re
import argparse
from task import Task
from shutil import copyfile, rmtree
from distutils.dir_util import copy_tree

filepath =  os.path.dirname(os.path.abspath(__file__))

class MnistFC(Task):
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument("--sparsity", default=None, type=float)
        self.h1_size, self.h2_size = 64, 64

    def replace_params(self, template, data):
        for k,v in data.items():
            kstr = "{{%s}}" % k
            template = template.replace(kstr, str(v))
        return template

    def generate_task(self, output_path, args):                
        assert(args.sparsity is not None)
        
        # Copy source files over
        source_files = ["%s/train" % filepath]
        for src in source_files:
            src_name = src.split("/")[-1]
            if os.path.isdir(src):
                copy_tree("%s" % src, output_path+"/"+src_name)
            else:
                copyfile(src, output_path + "/" + src_name) 

        # Run the script to generate hpp
        cmd = "bash train_and_generate.sh %d %d %f" % (self.h1_size, self.h2_size, args.sparsity)
        commands = ["cd %s/train && %s" % (output_path, cmd)]
        process = subprocess.Popen(commands, stdout=subprocess.PIPE, shell=True)
        out, err = process.communicate()
        out = out.decode('utf-8').strip()
        print(out)
        channeled_data = eval(out.splitlines()[-1])

        # Super hacky, but replace the src/main.cpp file with template
        # and insert args + results
        with open("%s/train/main.cpp" % output_path, "r") as f:
            template = f.read()
            template = self.replace_params(template, channeled_data)

        with open("%s/train/main.cpp" % output_path, "w") as f:
            f.write(template)
    
    def task_name(self):
        return "MnistFCSparsity"

    def get_parser(self):
        return self.parser
        
