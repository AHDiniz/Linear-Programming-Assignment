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

    print("maze created")

    model : Model = Model(name = 'Game Level Generator')

    
