from random import choice
from sys import argv
from gurobipy import *
from maze import Maze, Cell, CellType

def obj_func(tuples : list):
    result = 0
    for t in tuples:
        for y in tuples:
            result += t[0] - y[0] + t[1] - y[1]
    return result

def inequality_constraint(tuples : list, model : Model):
    

if len(argv) < 3:
    print("Usage: python main.py <<maze width>> <<maze height>>")
else:
    width : int = int(argv[1])
    height : int = int(argv[2])

    maze : Maze = Maze(width, height)
    maze.generate(0, 0)
    maze.set_different_cell_types()

    print("maze created")

    model : Model = Model(name = 'Game Level Generator')

    
