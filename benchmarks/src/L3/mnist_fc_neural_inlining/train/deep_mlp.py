#!/usr/bin/python
"""
# This script is based on:
# https://www.tensorflow.org/get_started/mnist/pros
"""
from __future__ import print_function
import sys
import json
import numpy as np
import os
import pickle
import tensorflow as tf
import argparse
from tensorflow.examples.tutorials.mnist import input_data
from tensorflow.python.framework import graph_util as gu
from tensorflow.tools.graph_transforms import TransformGraph

FLAGS = None

fc1_size = int(sys.argv[1])
fc2_size = int(sys.argv[2])
sparsity = float(sys.argv[3])

print("="*100)
print("RUNNING deep_mlp.py WITH FC1=%d, FC2=%d" % (fc1_size, fc2_size))
print("="*100)

# helper functions
def weight_variable(shape, name):
  """weight_variable generates a weight variable of a given shape."""
  initial = tf.truncated_normal(shape, stddev=0.1)
  return tf.Variable(initial, name)

def bias_variable(shape, name):
  """bias_variable generates a bias variable of a given shape."""
  initial = tf.constant(0.1, shape=shape)
  return tf.Variable(initial, name)

W_fc1, b_fc1, W_fc2, b_fc2, W_fc3, b_fc3 = None, None, None, None, None, None
assign_W1, assign_W2, assign_W3 = None, None, None
W1_pl, W2_pl, W3_pl = None, None, None

# Fully connected 2 layer NN
def deepnn(x):
  global W_fc1, b_fc1, W_fc2, b_fc2, W_fc3, b_fc3
  global assign_W1, assign_W2, assign_W3
  global W1_pl, W2_pl, W3_pl  

  tgt_fc1_size, tgt_fc2_size = fc1_size, fc2_size

  print("Using layer sizes: %d %d" % (fc1_size, fc2_size))

  W_fc1 = weight_variable([784//4, tgt_fc1_size], name='W_fc1')
  b_fc1 = bias_variable([tgt_fc1_size], name='b_fc1')
  a_fc1 = tf.add(tf.matmul(x, W_fc1), b_fc1, name="activations_1")
  h_fc1 = tf.nn.relu(a_fc1)
  layer1 = h_fc1

  W_fc2 = weight_variable([tgt_fc1_size, tgt_fc2_size], name='W_fc2')
  b_fc2 = bias_variable([tgt_fc2_size], name='b_fc2')
  a_fc2 = tf.add(tf.matmul(layer1, W_fc2), b_fc2, name="activations_2")
  h_fc2 = tf.nn.relu(a_fc2)
  layer2 = h_fc2

  W_fc3 = weight_variable([tgt_fc2_size, 10], name='W_fc3')
  b_fc3 = bias_variable([10], name='b_fc3')
  logits = tf.add(tf.matmul(layer2, W_fc3), b_fc3, name="logits")
  y_pred = tf.argmax(logits, 1, name='y_pred')

  W1_pl = tf.placeholder(tf.float32, W_fc1.get_shape().as_list())
  W2_pl = tf.placeholder(tf.float32, W_fc2.get_shape().as_list())
  W3_pl = tf.placeholder(tf.float32, W_fc3.get_shape().as_list())
  assign_W1 = tf.assign(W_fc1, W1_pl)
  assign_W2 = tf.assign(W_fc2, W2_pl)
  assign_W3 = tf.assign(W_fc3, W3_pl)

  return y_pred, logits

l1_scale = tf.placeholder(tf.float32)

def scale_image_smaller(x, factor=.5):
  interval = int(1/factor/factor)
  x_smaller = x[:,0:x.shape[1]:interval]
  return x_smaller

def main(_):
  # Import data
  mnist = input_data.read_data_sets(FLAGS.data_dir, one_hot=True)

  # Specify inputs, outputs, and a cost function
  # placeholders
  x = tf.placeholder(tf.float32, [None, 784//4], name="x")
  y_ = tf.placeholder(tf.float32, [None, 10], name="y")

  # Build the graph for the deep net
  y_pred, logits = deepnn(x)

  with tf.name_scope("Loss"):
    cross_entropy = tf.nn.softmax_cross_entropy_with_logits_v2(labels=y_,
                                                               logits=logits)
    loss = tf.reduce_mean(cross_entropy, name="cross_entropy_loss")
    l1_regularizer = tf.contrib.layers.l1_regularizer(
      scale=.999, scope=None
      )
    regularization_penalty = tf.contrib.layers.apply_regularization(l1_regularizer, [W_fc1, W_fc2, W_fc3])
    loss += l1_scale * regularization_penalty
    
  train_step = tf.train.AdamOptimizer(1e-4).minimize(loss, name="train_step")
  with tf.name_scope("Prediction"):
    correct_prediction = tf.equal(y_pred,
                                  tf.argmax(y_, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32), name="accuracy")

  l1_scale_scalar = 0

  # Start training session
  with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    saver = tf.train.Saver()

    # SGD
    for i in range(1, FLAGS.num_iter + 1):
      batch_images, batch_labels = mnist.train.next_batch(FLAGS.batch_size)
      feed_dict = {x: scale_image_smaller(batch_images), y_: batch_labels, l1_scale:l1_scale_scalar}
      train_step.run(feed_dict=feed_dict)
      if i % FLAGS.log_iter == 0:        
        W_1, b_1, W_2, b_2, W_3, b_3 = sess.run([W_fc1, b_fc1,
                                                 W_fc2, b_fc2,
                                                 W_fc3, b_fc3])
        if i >= 10000:
          W_1 = (1-((np.abs(W_1) < np.percentile(np.abs(W_1), sparsity)))) * W_1
          W_2 = (1-((np.abs(W_2) < np.percentile(np.abs(W_2), sparsity)))) * W_2
          W_3 = (1-((np.abs(W_3) < np.percentile(np.abs(W_3), sparsity)))) * W_3
          sess.run(assign_W1, feed_dict={W1_pl : W_1})
          sess.run(assign_W2, feed_dict={W2_pl : W_2})
          sess.run(assign_W3, feed_dict={W3_pl : W_3})
        train_accuracy = accuracy.eval(feed_dict=feed_dict)
        print('step %d, training accuracy %g (l1=%f)' % (i, train_accuracy, l1_scale_scalar))
        W_1, b_1, W_2, b_2, W_3, b_3 = sess.run([W_fc1, b_fc1,
                                                 W_fc2, b_fc2,
                                                 W_fc3, b_fc3])
        print("%d nnz of %d" % (np.count_nonzero(W_1), np.prod(W_1.shape)))
        print("%d nnz of %d" % (np.count_nonzero(W_2), np.prod(W_2.shape)))
        print("%d nnz of %d" % (np.count_nonzero(W_3), np.prod(W_3.shape)))


    acc = accuracy.eval(feed_dict={x: scale_image_smaller(mnist.test.images),
                                   y_: mnist.test.labels})
    print('test accuracy %g' % accuracy.eval(feed_dict={x: scale_image_smaller(mnist.test.images),
                                                        y_: mnist.test.labels}))
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

    
    W_1, b_1, W_2, b_2, W_3, b_3 = sess.run([W_fc1, b_fc1,
                                             W_fc2, b_fc2,
                                             W_fc3, b_fc3])
    d = {
      "W_1" : W_1,
      "W_2" : W_2,
      "W_3" : W_3,
      "b_1" : b_1,
      "b_2" : b_2,
      "b_3" : b_3
      }
    with open("weights", "wb") as f:
      pickle.dump(d, f)

    # Channelled data
    d = {
      "h1" : fc1_size,
      "h2" : fc2_size,
      "sparsity" : sparsity,
      "accuracy" : acc,
      }
    print(d)

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--data_dir', type=str,
                      default='mnist_data',
                      help='Directory for storing input data (default: %(default)s)')
  parser.add_argument('--chkp', default='chkps/mnist_model',
                      help='session check point (default: %(default)s)')
  parser.add_argument('-n', '--num-iteration', type=int,
                      dest='num_iter',
                      default=50000,
                      help='number of iterations (default: %(default)s)')
  parser.add_argument('--batch-size', dest='batch_size',
                      default=50, type=int,
                      help='batch size (default: %(default)s)')
  parser.add_argument('--log-every-iters', type=int,
                      dest='log_iter', default=1000,
                      help='logging the training accuracy per numbers of iteration %(default)s')
  parser.add_argument('--output-dir', default='mnist_model',
                      dest='output_dir',
                      help='output directory directory (default: %(default)s)')
  parser.add_argument('--no-quantization', action='store_true',
                      dest='no_quant',
                      help='save the output graph pb file without quantization')
  parser.add_argument('-o', '--output', default='deep_mlp.pb',
                      dest='pb_fname',
                      help='output pb file (default: %(default)s)')
  FLAGS, unparsed = parser.parse_known_args()
  tf.app.run(main=main, argv=[sys.argv[0]] + unparsed)
