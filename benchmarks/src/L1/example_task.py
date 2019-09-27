import sys
import argparse
from task import Task

class ExampleTask(Task):
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument("--param1", default=None, type=int)
        self.parser.add_argument("--param2", default=None, type=int)

    def generate_task(self, output_path, args):
        assert(args.param1 is not None)
        assert(args.param2 is not None)
        print("ExampleTask generating with params (%d, %d)" % 
              (args.param1, args.param2))

    def task_name(self):
        return "ExampleTask"

    def get_parser(self):
        return self.parser
        
