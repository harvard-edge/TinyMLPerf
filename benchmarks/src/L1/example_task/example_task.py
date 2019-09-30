import sys
import os
import re
import argparse
from task import Task

filepath =  os.path.dirname(os.path.abspath(__file__))
template_path = filepath + "/" + "template.c"

class ExampleTask(Task):
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument("--param1", default=None, type=int)
        self.parser.add_argument("--param2", default=None, type=int)

    def replace_with_params(self, template, param1, param2):
        assert("{{PARAM1}}" in template)
        assert("{{PARAM2}}" in template)
        template = template.replace("{{PARAM1}}", str(param1))
        template = template.replace("{{PARAM2}}", str(param2))
        return template

    def generate_task(self, output_path, args):
        assert(args.param1 is not None)
        assert(args.param2 is not None)
        with open(template_path, "r") as f:
            template_string = f.read()
        template_string = self.replace_with_params(template_string, 
                                                   args.param1, 
                                                   args.param2)
        with open(output_path + "/main.cpp", "w") as f:
            f.write(template_string)

    def task_name(self):
        return "ExampleTask"

    def get_parser(self):
        return self.parser
        
