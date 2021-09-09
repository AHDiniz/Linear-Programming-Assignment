from gurobipy import *
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import maximum_flow
from maze import Maze, Cell, CellType

maze : Maze = Maze(5, 4)
maze.generate(0, 0)
maze.set_different_cell_types()
print(maze.to_adj_matrix())
