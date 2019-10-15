import sys
import glob
import os
import re
import argparse
from task import Task
from shutil import copyfile
from distutils.dir_util import copy_tree

filepath =  os.path.dirname(os.path.abspath(__file__))
template_path = filepath + "/" + "template.c"

class MnistFC(Task):
    def __init__(self):
        self.parser = argparse.ArgumentParser()

    def generate_task(self, output_path, args):
        
        # Copy source files over
        source_files = glob.glob("%s/*[pp|h]" % filepath)
        for src in source_files:
            src_name = src.split("/")[-1]
            copyfile(src, output_path + "/" + src_name) 
        copy_tree("%s/src" % filepath, output_path+"/src")
    
    def task_name(self):
        return "MnistFC"

    def get_parser(self):
        return self.parser
        
