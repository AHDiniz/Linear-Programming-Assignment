import numpy as np
from random import choice
from sys import argv
from gurobipy import *
from maze import Maze, Cell, CellType

def capacity_constraint(capacity : dict, flow : tupledict, edge : tuple) -> TempConstr:
    return flow[edge] <= capacity[edge]

def key_flow_constraint(flow : tupledict, maze : Maze, index_dict : dict) -> TempConstr:
    print("Key Cell Codes: {key_mat_indexes}".format(key_mat_indexes=maze.key_mat_indexes))
    print("Index Dict: {dict}".format(dict=index_dict))
    key_indexes = index_dict[maze.key_mat_indexes[0]],index_dict[maze.key_mat_indexes[1]]
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

    player : Cell = maze.positions_of_type(CellType.PLAYER)[0]
    print("Player Cell Code : " + str(maze.cell_at(player[0], player[1]).cell_code))

    door : Cell = maze.positions_of_type(CellType.DOOR)[0]
    print("Door Cell Code : " + str(maze.cell_at(door[0], door[1]).cell_code))

    key : Cell = maze.positions_of_type(CellType.KEY)[0]
    print("Key Cell Code : " + str(maze.cell_at(key[0], key[1]).cell_code))

    enemies : list = maze.positions_of_type(CellType.ENEMY_1) + maze.positions_of_type(CellType.ENEMY_2) + maze.positions_of_type(CellType.ENEMY_3)
    for e in enemies:
        print("Enemy cell code : " + str(maze.cell_at(e[0], e[1]).cell_code))

    paths : list = maze.define_reduction_data()

    adj_matrix, index_dict = maze.to_reduced_adj_matrix()
    
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

    model.addConstr(key_flow_constraint(flow, maze, index_dict))
    

    for edge in edges:
        model.addConstr(capacity_constraint(capacities, flow, edge))
    
    model.setObjective(objective(costs, flow, edges), GRB.MINIMIZE)

    model.optimize()
