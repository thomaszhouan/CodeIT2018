import logging

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/customers-and-hotel/minimum-distance', methods=['POST'])
def min_dist():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    data = sorted(data)
    n = len(data)
    ans = -1
    for i in range(n-1):
        dis = data[i+1] - data[i]
        if ans < 0 or ans > dis:
            ans = dis
    if n == 1:
        ans = 0
    result = {'answer': ans}
    return jsonify(result)



