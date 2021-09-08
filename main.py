from gurobipy import *
from maze import Maze, Cell, CellType

maze : Maze = Maze(5, 4)
maze.generate(0, 0)
print(maze.to_adj_matrix())
