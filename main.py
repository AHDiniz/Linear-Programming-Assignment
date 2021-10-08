import numpy as np
from random import choice
from sys import argv
from gurobipy import *
from maze import Maze, Cell, CellType

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
    for row in range(adj_matrix.shape[0]):
        for column in range(adj_matrix.shape[1]):
            edge : tuple = (row, column)
            edges.append(edge)
            capacities[edge] = adj_matrix[row][column]
            costs[edge] = 1 if adj_matrix[row][column] == 1 else np.inf
    
    capacity = multidict(capacities)
    cost = multidict(costs)

    flow = model.addVars(edges, obj = cost[1], name = "flow")

    capacity_constraint = model.addConstrs(flow.select(edges[i][0], edges[i][1]) <= capacity[i] for i in range(len(edges)))

    key_indexes = maze.key_mat_indexes
    key_flow_constraint = model.addConstrs(flow.select(key_indexes[0], key_indexes[1]) == 1)

    model.setObjective(quicksum(flow.select(edges[i][0], edges[i][1]) * cost[i] for i in range(len(edges))), GRB.MINIMIZE)

    model.optimize()
