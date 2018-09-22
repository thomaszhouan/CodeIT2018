# -*- coding: utf-8 -*-
"""
Created on Sat Sep 22 21:41:14 2018

@author: zzhan
"""
import logging

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/broadcaster/message-broadcast', methods=['POST'])
def broadcaster_q1():
    data = request.get_json()
    # logging.info("data sent for evaluation {}".format(data))
    
    data = data.get("data")
    
    vertices = set()
    in_v = set()
    result = []
    for x in data:
        x, y = x.split("->")
        vertices.add(x)
        vertices.add(y)
        in_v.add(y)
    sources = vertices.difference(in_v)
    result = list(sources)
    final_result = {}
    final_result["result"] = result
    logging.info("My result :{}".format(final_result))
    return jsonify(final_result)



