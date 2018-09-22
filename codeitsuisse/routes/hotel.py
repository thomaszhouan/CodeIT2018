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
    result = {'answer': "%d" % ans}
    return jsonify(result)


@app.route('/customers-and-hotel/minimum-camps', methods=['POST'])
def min_camp():
    data = request.get_json()
    intervals = []
    for foo in data:
        a = foo.get('pos')
        b = foo.get('distance')
        intervals.append((a-b, a+b))
    intervals = sorted(intervals)
    ans = 0
    n = len(intervals)
    cur = -1000000000000000
    for i in range(n):
        if intervals[i][0] <= cur:
            continue
        cur = intervals[i][1]
        ans += 1
    return jsonify({'answer': ans})
