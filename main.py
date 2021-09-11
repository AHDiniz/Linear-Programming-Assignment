from random import choice
from sys import argv
from gurobipy import *
from maze import Maze, Cell, CellType

def avg_squared_distance(player : tuple, key : tuple, door : tuple, enemies : tuplelist) -> int:
    n : int = 2
    distance : int = (player[0] - key[0]) ** 2 + (player[1] - key[1]) ** 2
    distance += (player[0] - key[0]) ** 2 + (player[1] - key[1]) ** 2

    for enemy in enemies:
        distance += (player[0] - enemy[0]) ** 2 + (player[1] - enemy[1]) ** 2

    return distance / n

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

    # Variables that need to be set:
    # The player position
    playerX : Var = model.addVar(vtype = GRB.INTEGER, lb = 0, ub = width, name = 'playerX')
    playerY : Var = model.addVar(vtype = GRB.INTEGER, lb = 0, ub = height, name = 'playerY')
    player_pos : tuple = (playerX, playerY)

    print("model created and player variable")

    # The key position
    keyX : Var = model.addVar(vtype = GRB.INTEGER, lb = 0, ub = width, name = 'keyX')
    keyY : Var = model.addVar(vtype = GRB.INTEGER, lb = 0, ub = height, name = 'keyY')
    key_pos : tuple = (keyX, keyY)

    model.addConstr(playerX - keyX >= 1)
    model.addConstr(playerY - keyY >= 1)

    print("key variable")

    # The door position
    doorX : Var = model.addVar(vtype = GRB.INTEGER, lb = 0, ub = width, name = 'doorX')
    doorY : Var = model.addVar(vtype = GRB.INTEGER, lb = 0, ub = height, name = 'doorY')
    door_pos : tuple = (doorX, doorY)

    model.addConstr(playerX - doorX >= 1)
    model.addConstr(playerY - doorY >= 1)

    model.addConstr(keyX - doorX >= 1)
    model.addConstr(keyY - doorY >= 1)

    print("door variable")

    # The enemies positions
    enemies : tuplelist = tuplelist()
    for i in range(maze.enemy_count):
        enemyX : Var = model.addVar(vtype = GRB.INTEGER, lb = 0, ub = width, name = 'enemy' + str(i) + 'X')
        enemyY : Var = model.addVar(vtype = GRB.INTEGER, lb = 0, ub = height, name = 'enemy' + str(i) + 'Y')
        enemies.append((enemyX, enemyY))

        go_left : bool = choice([True, False])
        go_up : bool = choice([True, False])

        model.addConstr(playerX - enemyX >= 1)
        model.addConstr(playerY - enemyY >= 1)

        model.addConstr(keyX - enemyX >= 1)
        model.addConstr(keyY - enemyY >= 1)

        model.addConstr(doorX - enemyX >= 1)
        model.addConstr(doorY - enemyY >= 1)

    print("enemies variables")

    # Needs to maximize distance between player, key, door and enemies
    model.setObjective(avg_squared_distance(player_pos, key_pos, door_pos, enemies), GRB.MAXIMIZE)

    model.optimize()

    print("Player position = ", playerX.X, playerY.X)
    print("Key position = ", keyX.X, keyY.X)
    print("Door position = ", doorX.X, doorY.X)
    for enemy in enemies:
        print("Enemy position = ", enemy[0].X, enemy[1].X)
