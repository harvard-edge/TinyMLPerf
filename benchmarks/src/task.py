import sys

class Task(object):
    
    def __init__(self):
        pass

    def generate_task(self, output_path):
        raise NotImplementedError

    def task_name(self):
        raise NotImplementedError
