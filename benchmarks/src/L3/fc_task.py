import sys
import argparse
from task import Task
import tensorflow as tf
import numpy as np
from pathlib import Path


class FullyConnectedTask(Task):
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument("--param1", default=None, type=int)
        self.parser.add_argument("--param2", default=None, type=int)

    def generate_task(self, output_path, args):
        pass

    def task_name(self):
        return "FullyConnectedTask"

    def get_parser(self):
        return self.parser
    

class ReluTask(Task):
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument("--input-size", required=True, type=int,
                                 help="Input dimension to relu")

    def generate_task(self, output_path, args):
        input_size = args.input_size
        output_folder = Path(output_path) / 'input{}'.format(args.input_size)
        output_folder.mkdir(parents=True, exist_ok=True)
        with tf.Session() as sess:
            x = tf.placeholder(tf.float32, [None, input_size], name='input')
            output = tf.nn.relu(x, name='output')
            _ = output.eval(feed_dict={x: np.random.randn(1, input_size)})
            tf.train.write_graph(sess.graph_def, str(output_folder), 'model.pb')

    def task_name(self):
        return "ReluTask"

    def get_parser(self):
        return self.parser
 

if __name__ == '__main__':
    relu = ReluTask()
    args = relu.parser.parse_args()
    output_folder = Path('artifacts/relu')
    relu.generate_task(str(output_folder), args)
