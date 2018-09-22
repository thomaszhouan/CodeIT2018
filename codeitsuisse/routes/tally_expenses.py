import logging

from flask import request, jsonify

from codeitsuisse import app

import numpy as np
from decimal import localcontext, Decimal, ROUND_HALF_UP

logger = logging.getLogger(__name__)

def solve_tally(data):
    result = []
    persons = data.get('persons')
    n = 0
    p2id = {}
    for p in persons:
        p2id[p] = n
        n += 1
    with localcontext() as ctx:
        ctx.rounding = ROUND_HALF_UP
        exclude = [Decimal(0)] * n
        each = Decimal(0)
        expenses = data.get('expenses')
        for expense in expenses:
            tot = round(Decimal(expense.get('amount')), 2)
            if 'exclude' in expense:
                ex = expense.get('exclude')
                m = len(ex)
            else:
                ex = []
                m = 0
            assert m < n
            tmp = tot / (n-m)
            each += tmp
            i = p2id[expense.get('paidBy')]
            exclude[i] += tot
            for j in ex:
                i = p2id[j]
                exclude[i] += tmp

        for i in range(n-1):
            cur = each - exclude[i]
            cur = round(cur, 2)
            if cur > 0:
                result.append({
                    'from': persons[i],
                    'to': persons[i+1],
                    'amount': float(cur)
                })
                exclude[i+1] -= cur
            if cur < 0:
                result.append({
                    'from': persons[i+1],
                    'to': persons[i],
                    'amount': float(-cur)
                })
                exclude[i+1] -= cur

    return {'transactions': result}

@app.route('/tally-expense', methods=['POST'])
def tally_expense():
    data = request.get_json()
    return jsonify(solve_tally(data))