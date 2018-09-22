import logging
import collections
from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

boss = 0
visited = []
stack = [] # using list as stack to keep the minimum path
min_stack = []
min = 1e9

@app.route('/skill-tree', methods=['POST'])
def skill_tree():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    global visited
    global stack
    global boss
    global min_stack
    global min
    boss = data["boss"]["offense"]
    skills = {"root":0}
    inverse = {}
    graph = {0:{"n":[],"o":0,"p":0}}
    index = 1
    for skill in data["skills"]:
        skills[skill["name"]] = index
        inverse[index] = skill["name"]
        graph[index] = {"n":[], "o":skill["offense"], "p":skill["points"]}
        index += 1
    for skill in data["skills"]:
        r = skill["require"]
        n = skill["name"]
        if r == None:
            graph[0]["n"].append(skills[n])
        else:
            graph[skills[r]]["n"].append(skills[n])
    # print(graph)

    DFS(graph, 0, 0, 0)

    # print(min_stack)
    answer = []
    for m in min_stack:
        if(m != 0):
            answer.append(inverse[m])
    
    # print(answer)
    return jsonify(answer)


# DFS begins

def DFS(graph, node, sum, pnt):
    global visited
    global stack
    global boss
    global min_stack
    global min
    if node not in visited:
        visited.append(node)
        stack.append(node)
        # print("######", stack, "############")
        for n in graph[node]["n"]:
            if sum + graph[n]["o"] < boss:
                DFS(graph, n, sum + graph[n]["o"], pnt + graph[n]["p"])
            elif pnt + graph[n]["p"] < min:
                stack.append(n)
                min_stack = stack.copy()
                min = pnt + graph[n]["p"]
                stack.pop()
        stack.pop()

