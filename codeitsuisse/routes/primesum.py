import logging

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/prime-sum', methods=['POST'])
def primesum():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    x = data.get("input")
    r = x % 3
    q = x // 3
    if r == 0:
        result = []
    elif r == 1:
        result = [2, 2]
        q -= 1
    else:
        result = [2]
    result += [3] * q
    return jsonify(result)



