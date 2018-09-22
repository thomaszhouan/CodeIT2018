# -*- coding: utf-8 -*-
"""
Created on Sat Sep 22 09:53:26 2018

@author: zzhan
"""

import logging

from flask import request, jsonify

from codeitsuisse import app

import numpy as np

logger = logging.getLogger(__name__)

@app.route('/tally-expense', methods=['POST'])
def tally_expense():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    
    persons = data.get("persons")
    num_person = len(persons)
    money = {}
    for i in range(num_person):
        money[persons[i]] = 0
    expenses = data.get("expenses")
    for i in range(len(expenses)):
        temp = expenses[i]
        amount = temp["amount"]
        payer = temp["paidBy"]
        print(payer)
        if "exclude" in temp:
            exclude = temp["exclude"]
            num_pay = num_person - len(exclude)
            for j in persons:
                if not(j in exclude):
                    if j == payer:
                        money[j] += (num_pay - 1) * amount / num_pay
                    else:
                        money[j] -= amount / num_pay
        else:
            for j in persons:
                if j == payer:
                    money[j] += (num_person - 1) * amount / num_person
                else:
                    money[j] -= amount / num_person
    result = []
    transaction = np.zeros(num_person)
    for i in range(num_person):
        transaction[i] = money[persons[i]]
#    for i in range(num_person):
#        while transaction[i] != 0:
#            tran = transaction[i]
#            if transaction[i] > 0:               
#                minindex = np.argmin(transaction)
#                minm = transaction[minindex]
#                if tran + minm > 0:
#                    transaction[i] = tran + minm
#                    transaction[minindex] = 0
#                    temp = {}
#                    temp["from"] = persons[minindex]
#                    temp["to"] = persons[i]
#                    temp["amount"] = - minm
#                    result.append(temp)
#                else:
#                    transaction[i] = 0
#                    transaction[minindex] = tran + minm
#                    temp = {}
#                    temp["from"] = persons[minindex]
#                    temp["to"] = persons[i]
#                    temp["amount"] = tran
#                    result.append(temp)
#            else:
#                maxindex = np.argmax(transaction)
#                maxm = transaction[maxindex]
#                if tran + maxm > 0:
#                    transaction[i] = 0
#                    transaction[maxindex] = tran + maxm
#                    temp = {}
#                    temp["from"] = persons[i]
#                    temp["to"] = persons[maxindex]
#                    temp["amount"] = - tran
#                    result.append(temp)
#                else:
#                    transaction[maxindex] = 0
#                    transaction[i] = tran + maxm
#                    temp = {}
#                    temp["from"] = persons[i]
#                    temp["to"] = persons[maxindex]
#                    temp["amount"] = maxm
#                    result.append(temp)
                    
                    
    while max(transaction) > 0:
        maxindex = np.argmax(transaction)
        minindex = np.argmin(transaction)
        maxm = transaction[maxindex]
        minm = transaction[minindex]
        if maxm + minm > 0:
            transaction[maxindex] = maxm + minm
            transaction[minindex] = 0
            temp = {}
            temp["from"] = persons[minindex]
            temp["to"] = persons[maxindex]
            temp["amount"] = - minm
            result.append(temp)
        else:
            transaction[maxindex] = 0
            transaction[minindex] = maxm + minm
            temp = {}
            temp["from"] = persons[minindex]
            temp["to"] = persons[maxindex]
            temp["amount"] = maxm
            result.append(temp)
    final_result = {}
    final_result["transactions"] = result
    logging.info("My result :{}".format(final_result))
    return jsonify(final_result)

