import sys
from task import Task

class ExampleTask(Task):
    def __init__(self):
        pass

    def generate_task(self, output_path):
        print("ExampleTask starting...")

    def task_name(self):
        return "ExampleTask"

