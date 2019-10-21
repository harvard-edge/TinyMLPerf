import sys
import json
import numpy as np
import tensorflow as tf
import os
import argparse
from tensorflow.examples.tutorials.mnist import input_data
from utensor_cgen.frontend import FrontendSelector
from utensor_cgen.ir import uTensorGraph
import pickle as pkl

class Loader(object):

    def __init__(self, graphdef):

        # Initialize the model
        self.load_graph(graphdef)

    def load_graph(self, graph_def):
        '''
        Lode trained model.
        '''
        print('Loading model...')
        self.graph = tf.Graph()
        self.sess = tf.InteractiveSession(graph = self.graph)

        print('Check out the input placeholders:')
        print([n.name for n in graph_def.node])
        print([n.name + ' => ' +  n.op for n in graph_def.node])
        nodes = [n.name + ' => ' +  n.op for n in graph_def.node if n.op in ('Placeholder')]
        for node in nodes:
            print(node)

        # Define input tensor
        self.x = tf.placeholder(tf.float32, [None, 784], name="x")
        tf.import_graph_def(graph_def, {'x': self.x})

        print('Model loading complete!')

    def test(self, data):

        # Know your output node name
        output_tensor = self.graph.get_tensor_by_name("import/y_pred:0")
        output = self.sess.run(output_tensor, feed_dict = {self.x: data})

        return output

mnist = input_data.read_data_sets("mnist_data", one_hot=True)
fpath = sys.argv[1]
with open(fpath, "rb") as f:
    ugraph = pkl.load(f)
l = Loader(ugraph.graph_def)

preds = l.test(mnist.test.images)
truth = np.argmax(mnist.test.labels, axis=1)

# Accuracy and other params to channel
accuracy = np.sum(preds == truth) / preds.shape[0]
#print([op.values() for op in tf.get_default_graph().get_operations()])
d1 = l.graph.get_tensor_by_name("import/activations_1/eightbit/requantize:0").get_shape().as_list()[-1]
d2 = l.graph.get_tensor_by_name("import/activations_2/eightbit/requantize:0").get_shape().as_list()[-1]

# Dict with all params to channel
params_dict = {
    "accuracy" : accuracy,
    "h1" : d1,
    "h2" : d2,
    }
print(json.dumps(params_dict))
