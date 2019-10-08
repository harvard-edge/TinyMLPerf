import sys
import os
import re
import argparse

from task import Task

filepath =  os.path.dirname(os.path.abspath(__file__))
template_path = filepath + "/" + "template.c"

class ReadBytesTask(Task):
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument("--nbytes", default=None, type=int)

    def replace_with_params(self, template, bytes):
        assert("{{NBYTES}}" in template)
        template = template.replace("{{NBYTES}}", str(bytes))
        return template

    def generate_task(self, output_path, args):
        assert(args.nbytes is not None)
        with open(template_path, "r") as f:
            template_string = f.read()
        template_string = self.replace_with_params(template_string,
                                                   args.nbytes)
        with open(output_path + "/main.cpp", "w") as f:
            f.write(template_string)
    
    def task_name(self):
        return "ReadBytesTask"

    def get_parser(self):
        return self.parser
