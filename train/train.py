#!/bin/env python3
# -*- coding: utf8 -*-
import math

import click
import numpy as np
import tensorflow as tf

import torch
from model import build_graph, build_graph_2, build_fc_1
from torch import nn
from torchvision import transforms
from torchvision.datasets import cifar
from utensor_cgen.utils import prepare_meta_graph


def one_hot(labels, n_class=10):
    return np.eye(n_class)[labels]


def return_dataloader(batch_size):
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
        batch_size=1, shuffle=False, num_workers=2
    )
    return train_loader, eval_loader


@click.command()
@click.help_option("-h", "--help")
@click.option(
    "--batch-size", default=50, show_default=True, 
    help="the image batch size", type=int
)
@click.option(
    "--lr",
    default=0.9,
    show_default=True,
    help="the learning rate of the optimizer",
    type=float,
)
@click.option(
    "--epochs", default=10, show_default=True, 
    help="the number of epochs", type=int
)
@click.option(
    "--keep-prob",
    default=0.9,
    show_default=True,
    help="the dropout layer keep probability",
    type=float,
)
@click.option(
    "--chkp-dir",
    default="chkp/checkpoints",
    show_default=True,
    help="directory where to save check point files",
)
@click.option(
    "--output-pb",
    help="output model file name",
    default="output.pb",
    show_default=True,
)
@click.option(
    "--graph",
    help="Choice of neural network to use",
    show_default=True,
    default='1',
)
def train(batch_size, lr, epochs, keep_prob, chkp_dir, output_pb, graph):
    click.echo(
        click.style(
            "lr: {}, keep_prob: {}, output pbfile: {}".format(lr, keep_prob, output_pb),
            fg="cyan",
            bold=True,
        )
    )
    graph_object = graph  # will be overwritten by TF graph later

    train_loader, eval_loader = return_dataloader(batch_size)

    graph = tf.Graph()
    graph_builder_map = {
        'fc1': build_fc_1,
        '1': build_graph,
        '2': build_graph_2,
    }
    graph_builder = graph_builder_map[graph_object]

    with graph.as_default():
        tf_image_batch = tf.placeholder(tf.float32, shape=[None, 32, 32, 3])
        tf_labels = tf.placeholder(tf.float32, shape=[None, 10])
        tf_keep_prob = tf.placeholder(tf.float32, name="keep_prob")
        tf_pred, train_op, tf_total_loss, saver = graph_builder(
            tf_image_batch, tf_labels, tf_keep_prob, lr=lr
        )
    
    best_acc = 0.0
    chkp_cnt = 0

    with tf.Session(graph=graph) as sess:
        tf.global_variables_initializer().run()
        for epoch in range(1, epochs + 1):
            for i, training_batch in enumerate(train_loader, 1):
                img_batch, label_batch = training_batch
                np_img_batch = img_batch.numpy()
                np_label_batch = np.array(label_batch)
                _ = sess.run(
                    train_op,
                    feed_dict={
                        tf_image_batch: np_img_batch,
                        tf_labels: one_hot(np_label_batch),
                        tf_keep_prob: keep_prob,
                    },
                )

                if (i % 100) == 0:
                    correct, total = 0, 0
                    for img_batch, label_batch in eval_loader:
                        np_img_batch = img_batch.numpy()
                        np_label_batch = label_batch.numpy()
                        pred_label = sess.run(
                            tf_pred,
                            feed_dict={tf_image_batch: np_img_batch, tf_keep_prob: 1.0},
                        )
                        correct += (pred_label == np_label_batch).sum()
                        total += np_label_batch.shape[0]
                        acc = correct / float(total)
                    
                    click.echo(
                        click.style(
                            "[epoch {}: {}], accuracy {:0.2f}%".format(
                                epoch, i, acc * 100
                            ),
                            fg="yellow",
                            bold=True,
                        )
                    )

                    if acc >= best_acc:
                        best_acc = acc
                        chkp_cnt += 1
                        click.echo(
                            click.style(
                                "[epoch {}: {}] saving checkpoint, {} with acc {:0.2f}%".format(
                                    epoch, i, chkp_cnt, best_acc * 100
                                ),
                                fg="white",
                                bold=True,
                            )
                        )
                        best_chkp = saver.save(sess, chkp_dir, global_step=chkp_cnt)


    best_graph_def = prepare_meta_graph(
        "{}.meta".format(best_chkp), output_nodes=[tf_pred.op.name]
    )

    with open(output_pb, "wb") as fid:
        fid.write(best_graph_def.SerializeToString())
        click.echo(click.style("{} saved".format(output_pb), fg="blue", bold=True))


if __name__ == "__main__":
    train()
