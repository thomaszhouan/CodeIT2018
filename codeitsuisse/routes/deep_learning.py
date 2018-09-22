# -*- coding: utf-8 -*-
"""
Created on Sat Sep 22 14:48:01 2018

@author: zzhan
"""
import numpy as np

import logging

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

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


