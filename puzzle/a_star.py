import numpy as np
import json


DIRECTIONS = {
    'North': (-1, 0),
    'South': (+1, 0),
    'West': (0, -1),
    'East': (0, +1)
}


class Node:
    def __init__(self, state:np.array, parent:np.array, move:str, h_cost:int, g_cost:int) -> None:
        self.state = state.copy()
        self.parent = parent.copy()
        self.state_str = np.array_str(state)
        self.parent_str = np.array_str(parent)
        self.move = move
        self.h_cost = h_cost
        self.g_cost = g_cost
        self.f_cost = h_cost + g_cost


def get_index(matrix:np.array, element:int) -> tuple:
    row, col = np.where(matrix == element)
    return (int(row), int(col))


# manhattan distance
def h(current:np.array, goal:np.array) -> int:
    h_cost = 0
    for current_y in range(current.shape[0]):
        for current_x in range(current.shape[1]):
            goal_y, goal_x = get_index(goal, current[current_y][current_x])
            h_cost += abs(current_x - goal_x) + abs(current_y - goal_y)
    return h_cost


def get_best_node(collection:dict) -> Node:
    first = True
    for node in collection.values():
        if first or node.f_cost < f_best:
            first = False
            node_best = node
            f_best = node.f_cost
    return node_best


def get_children(node:Node, goal:np.array) -> list:

    zero_y, zero_x = get_index(node.state, 0)
    successors = []

    for direction in DIRECTIONS.keys():
        new_y, new_x = zero_y + DIRECTIONS[direction][0], zero_x + DIRECTIONS[direction][1]
        if 0 <= new_y < node.state.shape[0] and 0 <= new_x < node.state.shape[1]:
            new_state = node.state.copy()
            new_state[new_y][new_x], new_state[zero_y][zero_x] = new_state[zero_y][zero_x], new_state[new_y][new_x]
            successors.append(Node(new_state, node.state, direction, h(new_state, goal), node.g_cost+1))

    return successors


def get_process(exploration:dict, goal:np.array) -> tuple:

    step = exploration[np.array_str(goal)]
    path = []

    while step.move:
        path.append(step.move)
        step = exploration[step.parent_str]
    path.reverse()

    return exploration, path


# searching algorithm
def a_star(start:np.array, goal:np.array) -> tuple:

    open = {np.array_str(start): Node(start, start, '', h(start, goal), 0)}
    closed = {}

    while True:

        node_best = get_best_node(open)
        closed[node_best.state_str] = node_best

        if np.array_equal(node_best.state, goal):
            return get_process(closed, goal)

        adjacent_nodes = get_children(node_best, goal)
        for node in adjacent_nodes:
            if node.state_str in closed.keys() or node.state_str in open.keys() and open[node.state_str].f_cost < node.f_cost:
                continue
            open[node.state_str] = node

        del open[node_best.state_str]


# main
if __name__ == '__main__':

    try:
        with open('input.json', 'r') as input:
            data = json.load(input)
    except:
        raise Exception('input.json could not be opened')

    start = np.array(data['start'])
    goal = np.array(data['goal'])

    search, path = a_star(start, goal)

    summary = {}
    summary['Searching Algorithm'] = 'A*'
    summary['Search Length'] = len(search)
    summary['Path Length'] = len(path)
    summary['Path'] = path

    try:
        with open('output.json', 'w') as output:
            json.dump(summary, output, indent=4)
    except:
        raise Exception('output.json could not be created')