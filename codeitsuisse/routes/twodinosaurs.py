import logging
import numpy as np
from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)


def solve_dp(A):
    mod = 100000123
    maxn = 400010
    dp = [0] * maxn
    dp[0] = 1
    cur = 0
    for a in A:
        cur += a
        for i in range(cur,-1,-1):
            j = i - a
            if j < 0:
                break
            dp[i] += dp[j]
            if dp[i]>=mod:
                dp[i] -= mod
    return dp


def solve_dino(n, A, B, q):
    a = solve_dp(A)
    b = solve_dp(B)
    return a, b


@app.route('/two-dinosaurs', methods=['POST'])
def dinosaur():
    data = request.get_json()
    # logging.info("data sent for evaluation {}".format(data))
    N = data["number_of_types_of_food"]
    listA = data["calories_for_each_type_for_raphael"]
    listB = data["calories_for_each_type_for_leonardo"]
    Q = data["maximum_difference_for_calories"]
    mod = 100000123

    p1, p2 = solve_dino(N, listA, listB, Q)
    l2 = len(p2)
    l1 = len(p1)
    # if False: # old
    #     p1 = np.poly1d([1])
    #     for a in listA:
    #         pt = np.zeros(a+1)
    #         pt[0] = 1
    #         pt[a] = 1
    #         p1 = np.fmod(np.polymul(p1, pt), mod) # this is an np array, not np.poly1d
    #     # print(p1)
    #     p2 = np.poly1d([1])
    #     for b in listB:
    #         ps = np.zeros(b+1)
    #         ps[0] = 1
    #         ps[b] = 1
    #         p2 = np.fmod(np.polymul(p2, ps), mod)
    #     # print(p2)
    #     # sliding windo
    #     l1 = p1.size
    #     l2 = p2.size
    #     if l1 < l2:
    #         p3 = np.zeros(l2)
    #         p3[-l1:] = p1
    #         p1 = p2
    #         p2 = p3
    #         l1 = p1.size
    #     elif l1 > l2:
    #         p3 = np.zeros(l1)
    #         p3[-l2:] = p2
    #         p2 = p3
    #         l2 = p2.size

    # print(p1)
    # print(p2)
    # preprocessing, so that first term of l1 is not zero
    answer = 0
    sum = 0
    ub = min(l2 - 1, Q)
    lb = 0
    for j in range(lb, ub + 1):
        sum = (sum + p2[j]) % mod
    answer = sum * p1[0] % mod
    # print(sum)
    for index in range(1,l1):
        if index - Q > 0:
            # update left
            sum = (mod + sum - p2[index - Q - 1]) % mod
        if index + Q < l1:
            # update right
            sum = (sum + p2[index + Q]) % mod
        # print(sum)
        temp = p1[index] * sum % mod
        answer = (temp+answer)%mod
    return jsonify({"result":answer}) 