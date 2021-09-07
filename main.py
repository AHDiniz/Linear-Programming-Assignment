from gurobipy import *
from maze import Maze, Cell, CellType

maze : Maze = Maze(60, 60)
maze.generate(29, 29)
print(maze.to_adj_matrix())
