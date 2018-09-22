# -*- coding: utf-8 -*-
"""
Created on Sat Sep 22 21:41:14 2018

@author: zzhan
"""
import queue

import logging

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/broadcaster/message-broadcast', methods=['POST'])
def broadcaster_q1():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    
    data = data.get("data")
    
    vertices = set()
    in_v = set()
    graph = {}
    in_number = {}
    result = []
    for x in data:
        x, y = x.split("->")
        vertices.add(x)
        vertices.add(y)
        in_v.add(y)
        if x in graph:
            if not(y in graph[x]):
                graph[x].append(y)
        else:
            graph[x] = [y]
        if y in in_number:
            in_number[y] += 1
        else:
            in_number[y] = 1
    sources = vertices.difference(in_v)
    result = list(sources)
    logging.info("My result :{}".format(result))
    return jsonify(result)



