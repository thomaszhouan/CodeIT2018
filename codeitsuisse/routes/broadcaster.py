# -*- coding: utf-8 -*-
"""
Created on Sat Sep 22 17:31:36 2018

@author: zzhan
"""

import logging

from flask import request, jsonify

from codeitsuisse import app

import queue

logger = logging.getLogger(__name__)

@app.route('/broadcaster/most-connected-node', methods=['POST'])
def most_connected_node():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    data = data.get("data")
    graph = {}
    for x in data:
        x, y = x.split("->")
        if x in graph:
            if not(y in graph[x]):
                graph[x].append(y)
        else:
            graph[x] = [y]
    q = queue.Queue()
    
    node = None
    maxlen = 0
    for x in graph:
        q = queue.Queue()
        for y in graph[x]:
            q.put(y)
        while not q.empty():
            y = q.get()
            if y in graph:
                for z in graph[y]:
                    if not (z in q.queue):
                        q.put(z)
                    if not (z in graph[x]):
                        graph[x].append(z)
        if len(graph[x]) > maxlen:
            maxlen = len(graph[x])
            node = x
    result = {}
    result["result"] = node
    logging.info("My result :{}".format(result))
    return jsonify(result)



