from sys import argv
from gurobipy import *
from maze import Maze, Cell, CellType

def avg_distance(variables : dict) -> int:
    

    return 0

if __name__ == '__main__':
    if len(argv) < 2:
        print("Usage: python main.py <<maze width>> <<maze height>>")
    elif len(argv) == 2:
        width : int = int(argv[0])
        height : int = int(argv[1])
    
        maze : Maze = Maze(width, height)
        maze.generate(0, 0)
        maze.set_different_cell_types()

        lin_prog_model : Model = Model(name = 'Game Level Generator')

        # Variables that need to be set:
        # The player position
        # The key position
        # The door position
        # The enemies positions
        # Needs to maximize distance between player, key, door and enemies
        # Needs to stay in the limits of the graph
        # Every position needs to be different from each other

    
