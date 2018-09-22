# -*- coding: utf-8 -*-
"""
Created on Sat Sep 22 17:31:36 2018

@author: zzhan
"""

import logging

from flask import request, jsonify

from codeitsuisse import app

import queue
import heapq

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


def solve_shortest_path(data):
    node2id = {}
    nodes = []

    def get_id(node):
        if node in node2id:
            return node2id[node]
        n = len(node2id)
        node2id[node] = n
        nodes.append(node)
        return n

    edge = []
    # print(data['data'])
    for foo in data['data']:
        foo0, w = foo.split(',')
        u, v = foo0.split('->')
        u = get_id(u)
        v = get_id(v)
        w = int(w)
        edge.append((u, v, w))
    # print(edge)
    # print(nodes)
    # print(node2id)

    n = len(node2id)
    g = []
    for i in range(n):
        g.append([])
    for i, (u, _, _) in enumerate(edge):
        g[u].append(i)
    # print(g)

    p = [-1] * n
    d = [-1] * n
    vis = [False] * n
    s = get_id(data['sender'])
    t = get_id(data['recipient'])
    q = [(0, s)]
    heapq.heapify(q)
    d[s] = 0
    while len(q) > 0:
        foo = heapq.heappop(q)
        u = foo[1]
        if vis[u]:
            continue
        vis[u] = True
        if u == t:
            path = []
            while u != -1:
                path.append(nodes[u])
                u = p[u]
            return list(reversed(path))
        for i in g[u]:
            _, v, w = edge[i]
            if d[v]<0 or d[v]>w+d[u]:
                d[v] = w+d[u]
                p[v] = u
                heapq.heappush(q, (d[v], v))
    assert False


@app.route('/broadcaster/fastest-path', methods=['POST'])
def fastest_path():
    data = request.get_json()
    return jsonify({'result': solve_shortest_path(data)})
