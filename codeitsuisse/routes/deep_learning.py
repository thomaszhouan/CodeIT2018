# -*- coding: utf-8 -*-
"""
Created on Sat Sep 22 14:48:01 2018

@author: zzhan
"""
import numpy as np
import tensorflow as tf
from tensorflow.keras.datasets import mnist

import logging

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Model:
    def __init__(self):
        self.input_X = tf.placeholder(tf.float32, [None, 784])
        self.input_y = tf.placeholder(tf.int32)

        self.hidden1 = tf.layers.dense(inputs=self.input_X, units=1024, activation=tf.nn.relu)
        self.hidden2 = tf.layers.dense(inputs=self.hidden1, units=1024, activation=tf.nn.relu)
        self.logits = tf.layers.dense(inputs=self.hidden2, units=10, activation=None)

        self.prediction = tf.argmax(self.logits, axis=1, output_type=tf.int32)
        self.loss = tf.nn.sparse_softmax_cross_entropy_with_logits(labels=self.input_y, logits=self.logits)
        self.loss = tf.reduce_mean(self.loss)
        self.accuracy = tf.reduce_mean(tf.cast(tf.equal(self.prediction, self.input_y), tf.float32))

def batch_generator(X, y, shuffle=True, batch_size=64):
    n = X.shape[0]
    n_batch = (n-1)//batch_size + 1

    shuffle_idx = np.arange(n)
    if shuffle:
        shuffle_idx = np.random.permutation(shuffle_idx)
    X = X[shuffle_idx]
    y = y[shuffle_idx]

    for batch in range(n_batch):
        start = batch * batch_size
        end = (batch+1) * batch_size
        yield X[start:end], y[start:end], batch


logger.info('Constructing model')
model = Model()
(X_train, y_train), (X_test, y_test) = mnist.load_data()
X_train = X_train.reshape([-1, 784]).astype(np.float32)
X_test = X_test.reshape([-1, 784]).astype(np.float32)
X_mean = np.mean(X_train, axis=0)
X_train -= X_mean
X_test -= X_mean
X_train /= 128
X_test /= 128
optimizer = tf.train.MomentumOptimizer(learning_rate=1e-2, momentum=0.95)
train_op = optimizer.apply_gradients(optimizer.compute_gradients(model.loss))
init_op = tf.global_variables_initializer()
logger.info('Start training..')
with tf.Session() as sess:
    sess.run(init_op)

    for epoch in range(2):
        logger.info('Epoch %d' % (epoch+1))
        for X, y, b in batch_generator(X_train, y_train):
            _, loss, acc = sess.run([train_op, model.loss, model.accuracy], feed_dict={model.input_X: X, model.input_y: y})
            if (b+1) % 100 == 0:
                logger.info('Batch %d loss %f' % (b+1, loss))
        loss, acc = sess.run([model.loss, model.accuracy], feed_dict={model.input_X: X_test, model.input_y: y_test})
        logger.info('Epoch %d test loss %f accuracy %f' % (epoch+1, loss, acc))


@app.route('/machine-learning/question-1', methods=['POST'])
def linear_regression():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    X = np.array(data.get("input"))
    y = np.array(data.get("output"))
    test = np.array(data.get("question"))
    w = np.linalg.inv(X.T @ X) @ X.T @ y
    y_pred = test @ w
    result = {}
    result["answer"] = y_pred
    logging.info("My result :{}".format(result))
    return jsonify(result)


@app.route('/machine-learning/question-2', methods=['POST'])
def mnist_lol():
    data = request.get_json()['question']
    data = np.array(data).astype(np.float)
    data -= X_mean
    data /= 128
    pred = None
    with tf.Session() as sess:
        pred = sess.run(model.prediction, feed_dict={model.input_X: data})
    result = {'answer': pred.tolist()}
    return jsonify(result)
