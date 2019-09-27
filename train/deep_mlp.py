#!/usr/bin/python
# -*- coding: utf8 -*-
"""
# This script is based on:
# https://www.tensorflow.org/get_started/mnist/pros
"""
from __future__ import print_function
import argparse
import sys
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
from tensorflow.python.framework import graph_util as gu
from tensorflow.tools.graph_transforms import TransformGraph
import numpy as np

FLAGS = None

import torch
from torch import nn
from torchvision import transforms
from torchvision.datasets import cifar


def one_hot(labels, n_class=10):
        return np.eye(n_class)[labels]

def return_dataloader(dataset, batch_size):
        """Returns pytorch dataloaders for train and test. We expect the dataloader
        to contain numpy arrays corresponding to images, along with categorical
        labels. Returns the train, eval dataloaders as a tuple."""
        cifar10_train = cifar.CIFAR10("~/.cifar10_data", download=True, train=True)
        cifar10_test = cifar.CIFAR10("~/.cifar10_data", download=True, train=False)

        cifar10_train_image = [np.array(x[0]) for x in cifar10_train]
        cifar10_train_label = [x[1] for x in cifar10_train]
        cifar10_test_image = [np.array(x[0]) for x in cifar10_test]
        cifar10_test_label = [x[1] for x in cifar10_test]

        train_loader = torch.utils.data.DataLoader(
                list(zip(cifar10_train_image, cifar10_train_label)),
                batch_size=batch_size, shuffle=True, num_workers=2
        )
        eval_loader = torch.utils.data.DataLoader(
                list(zip(cifar10_test_image, cifar10_test_label)),
                batch_size=len(cifar10_test_image), shuffle=False, num_workers=2
        )
        return train_loader, eval_loader

# helper functions
def weight_variable(shape, name):
    """weight_variable generates a weight variable of a given shape."""
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial, name)


def bias_variable(shape, name):
    """bias_variable generates a bias variable of a given shape."""
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial, name)


# Fully connected 2 layer NN

def deepnn_fc1(x):
    return deepnn(x, 128, 64)

def deepnn_fc2(x):
    return deepnn(x, 256, 64)

def deepnn_fc3(x):
    return deepnn(x, 256, 128)


def deepnn(x, first_layer, second_layer):
    W_fc1 = weight_variable([32 * 32 * 3, first_layer], name='W_fc1')
    b_fc1 = bias_variable([first_layer], name='b_fc1')
    a_fc1 = tf.add(tf.matmul(x, W_fc1), b_fc1, name="zscore")
    h_fc1 = tf.nn.relu(a_fc1)
    layer1 = tf.nn.dropout(h_fc1, 0.50)

    W_fc2 = weight_variable([first_layer, second_layer], name='W_fc2')
    b_fc2 = bias_variable([second_layer], name='b_fc2')
    a_fc2 = tf.add(tf.matmul(layer1, W_fc2), b_fc2, name="zscore")
    h_fc2 = tf.nn.relu(a_fc2)
    layer2 = tf.nn.dropout(h_fc2, 0.50)

    W_fc3 = weight_variable([second_layer, 10], name='W_fc3')
    b_fc3 = bias_variable([10], name='b_fc3')
    logits = tf.add(tf.matmul(layer2, W_fc3), b_fc3, name="logits")
    y_pred = tf.argmax(logits, 1, name='y_pred')

    return y_pred, logits


def main(_):

    train_dataloader, test_dataloader = return_dataloader('cifar', 32)

    # Specify inputs, outputs, and a cost function
    # placeholders
    x = tf.placeholder(tf.float32, [None, 32 * 32 * 3], name="x")
    y_ = tf.placeholder(tf.float32, [None, 10], name="y")

    # Build the graph for the deep net
    # neural_network_map = {
    #     'fc1': deepnn_fc1,
    #     'fc2': deepnn_fc2,
    #     'fc3': deepnn_fc3,
    # }
    # neural_network = neural_network_map[FLAGS.models]
    # y_pred, logits = neural_network(x)
    y_pred, logits = deepnn(x, FLAGS.first_layer, FLAGS.second_layer)

    with tf.name_scope("Loss"):
        cross_entropy = tf.nn.softmax_cross_entropy_with_logits_v2(labels=y_,
                                                                                                                             logits=logits)
        loss = tf.reduce_mean(cross_entropy, name="cross_entropy_loss")
    train_step = tf.train.AdamOptimizer(1e-4).minimize(loss, name="train_step")

    with tf.name_scope("Prediction"):
        correct_prediction = tf.equal(y_pred,
                                                                    tf.argmax(y_, 1))
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32), name="accuracy")

    # Start training session
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        saver = tf.train.Saver()

        # SGD
        for epoch in range(1):
            for batch_images, batch_labels in train_dataloader:
                    batch_images, batch_labels = batch_images.numpy(), batch_labels.numpy()
                    batch_images = batch_images.reshape(batch_images.shape[0], -1)
                    batch_labels = one_hot(batch_labels)
                    feed_dict = {x: batch_images, y_: batch_labels}
                    train_step.run(feed_dict=feed_dict)

            test_images, test_labels = next(iter(test_dataloader))
            test_images, test_labels = test_images.numpy(), test_labels.numpy()
            test_images = test_images.reshape(test_images.shape[0], -1)
            test_labels = one_hot(test_labels)
            print('test accuracy %g' % accuracy.eval(feed_dict={x: test_images,
                                                                                                                y_: test_labels}))
        # Saving checkpoint and serialize the graph
        ckpt_path = saver.save(sess, FLAGS.chkp)
        print('saving checkpoint: %s' % ckpt_path)
        out_nodes = [y_pred.op.name]
        # Freeze graph and remove training nodes
        sub_graph_def = gu.remove_training_nodes(sess.graph_def)
        sub_graph_def = gu.convert_variables_to_constants(sess, sub_graph_def, out_nodes)
        if FLAGS.no_quant:
            graph_path = tf.train.write_graph(sub_graph_def,
                                                                                FLAGS.output_dir,
                                                                                FLAGS.pb_fname,
                                                                                as_text=False)
        else:
            # # quantize the graph
            # quant_graph_def = TransformGraph(sub_graph_def,
            #                                  [],
            #                                  out_nodes,
            #                                  ["quantize_weights", "quantize_nodes"])
            graph_path = tf.train.write_graph(sub_graph_def,
                                                                                FLAGS.output_dir,
                                                                                FLAGS.pb_fname,
                                                                                as_text=False)
        print('written graph to: %s' % graph_path)
        print('the output nodes: {!s}'.format(out_nodes))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_dir', type=str,
                        default='~/.mnist_data',
                        help='Directory for storing input data (default: %(default)s)')
    parser.add_argument('--chkp', default='chkps/mnist_model',
                        help='session check point (default: %(default)s)')
    parser.add_argument('-n', '--num-iteration', type=int,
                        dest='num_iter',
                        default=20000,
                        help='number of iterations (default: %(default)s)')
    parser.add_argument('--batch-size', dest='batch_size',
                        default=50, type=int,
                        help='batch size (default: %(default)s)')
    parser.add_argument('--log-every-iters', type=int,
                        dest='log_iter', default=1000,
                        help='logging the training accuracy per numbers of iteration %(default)s')
    parser.add_argument('--output-dir', default='models',
                        dest='output_dir',
                        help='output directory directory (default: %(default)s)')
    parser.add_argument('--no-quantization', action='store_true',
                        dest='no_quant',
                        help='save the output graph pb file without quantization')
    parser.add_argument('--model', default='fc1',
                        dest='models',
                        help='Type of model to use.')
    parser.add_argument('-o', '--output', default='model.pb',
                        dest='pb_fname',
                        help='output pb file (default: %(default)s)')
    parser.add_argument('--first-layer', default=128, type=int,
                        dest='first_layer',
                        help='number of weights in first layer')
    parser.add_argument('--second-layer', default=64, type=int,
                        dest='second_layer',
                        help='number of weights in second layer')
    FLAGS, unparsed = parser.parse_known_args()
    FLAGS, unparsed = parser.parse_known_args()
    FLAGS, unparsed = parser.parse_known_args()
    tf.app.run(main=main, argv=[sys.argv[0]] + unparsed)
