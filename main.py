import numpy as np
from random import choice
from sys import argv
from gurobipy import *
from maze import Maze, Cell, CellType

def capacity_constraint(capacity : dict, flow : tupledict, edge : tuple) -> TempConstr:
    return flow[edge] <= capacity[edge]

def key_flow_constraint(flow : tupledict, maze : Maze) -> TempConstr:
    key_indexes = maze.key_mat_indexes
    return flow[key_indexes] == 1

def objective(cost : dict, flow : tupledict, edges : list) -> LinExpr:
    print(cost[edges[0]])
    result : LinExpr = cost[edges[0]] * flow[edges[0]]
    for i in range(1, len(edges)):
        result += cost[edges[i]] * flow[edges[i]]
    return result

if len(argv) < 3:
    print("Usage: python main.py <<maze width>> <<maze height>>")
else:
    width : int = int(argv[1])
    height : int = int(argv[2])

    maze : Maze = Maze(width, height)
    maze.generate(0, 0)
    maze.set_different_cell_types()

    adj_matrix : np.ndarray = maze.to_adj_matrix()

    print(adj_matrix)

    print("The maze was generated.")

    model : Model = Model(name = 'Game Level Playability Checker')

    print("The optimization model was created.")

    capacities : dict = {}
    costs : dict = {}
    edges : list = []

    enemy_positions : list = maze.enemies_mat_indexes

    for row in range(adj_matrix.shape[0]):
        for column in range(adj_matrix.shape[1]):
            edge : tuple = (row, column)
            edges.append(edge)
            capacities[edge] = adj_matrix[row][column]
            costs[edge] = 1 if (row, column) in enemy_positions else 99

    flow = model.addVars(edges, name = "flow")

    model.addConstr(key_flow_constraint(flow, maze))

    for edge in edges:
        model.addConstr(capacity_constraint(capacities, flow, edge))
    
    model.setObjective(objective(costs, flow, edges), GRB.MINIMIZE)

    model.optimize()
