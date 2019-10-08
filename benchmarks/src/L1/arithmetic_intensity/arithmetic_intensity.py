import sys
import os
import re
import argparse

from task import Task

filepath =  os.path.dirname(os.path.abspath(__file__))
template_path = filepath + "/" + "template.c"

class ArithmeticIntensity(Task):
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument("--nfloats", default=None, type=int, required=True)
        self.parser.add_argument("--arith_intens", default=None, type=float, required=True)
        self.parser.add_argument("--nreps", default=100, type=int)

    def replace_with_params(self, template, floats, n_reps, arith_intens):
        assert("{{NFLOATS}}" in template)
        assert("{{AI}}" in template)
        assert("{{N_REPS}}" in template)
        template = template.replace("{{NFLOATS}}", str(floats))
        template = template.replace("{{AI}}", str(arith_intens))
        template = template.replace("{{N_REPS}}", str(n_reps))
        return template

    def generate_task(self, output_path, args):
        with open(template_path, "r") as f:
            template_string = f.read()
        template_string = self.replace_with_params(template_string,
                                                   args.nfloats,
                                                   args.nreps,
                                                   args.arith_intens)
        with open(output_path + "/main.cpp", "w") as f:
            f.write(template_string)
    
    def task_name(self):
        return "ArithmeticIntensityTask"

    def get_parser(self):
        return self.parser
