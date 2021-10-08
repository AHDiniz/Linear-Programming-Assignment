import numpy as np
import random
from enum import Enum
from math import inf

class CellType(Enum):
    NONE = 0
    PLAYER = 1
    ENEMY_1 = 2
    ENEMY_2 = 3
    ENEMY_3 = 4
    KEY = 5
    DOOR = 6

class Cell:
    wall_pairs = {'N' : 'S', 'S' : 'N', 'E' : 'W', 'W' : 'E'}

    def __init__(self, cell_code: int, x : int, y : int, cell_type : CellType):
        self.__cell_code : int = cell_code
        self.__x : int = x
        self.__y : int = y
        self.__walls : dict = {'N': True, 'S': True, 'E': True, 'W': True}
        self.__cell_type : CellType = cell_type
    
    @property
    def x(self) -> int:
        return self.__x
    
    @property
    def y(self) -> int:
        return self.__y
    
    @property
    def cell_code(self) -> int:
        return self.__cell_code
    
    @property
    def cell_walls(self) -> dict:
        return self.__walls
    
    def get_cell_type(self) -> CellType:
        return self.__cell_type
    
    def set_cell_type(self, cell_type : CellType):
        self.__cell_type = cell_type
    
    cell_type = property(get_cell_type, set_cell_type)

    def has_all_walls(self):
        return all(self.__walls.values())
    
    def knock_down_wall(self, other, wall : str):
        self.__walls[wall] = False
        other.__walls[Cell.wall_pairs[wall]] = False

class Maze:
    def __init__(self, rows : int, columns : int, enemy_count : int = 3):
        self.__rows : int = rows
        self.__columns : int = columns
        self.__map : list = list([])
        self.__enemy_count : int = enemy_count
        self.__adj_matrix : list = None

        self.__player_cell_code : int = -1
        self.__door_cell_code : int = -1

        self.__key_mat_indexes : tuple = None
        self.__enemies_mat_indexes : list = []

        for i in range(self.__rows):
            self.__map.append(list([]))
            for j in range(self.__columns):
                self.__map[i].append(Cell((i * self.__columns + j), i, j, CellType.NONE))

    @property
    def enemy_count(self) -> int:
        return self.__enemy_count
    
    @property
    def key_mat_indexes(self) -> tuple:
        return self.__key_mat_indexes
    
    @property
    def enemies_mat_indexes(self) -> list:
        return self.__enemies_mat_indexes
    
    @property
    def player_cell_code(self) -> int:
        return self.__player_cell_code
    
    @property
    def door_cell_code(self) -> int:
        return self.__door_cell_code

    def cell_at(self, x : int, y : int) -> Cell:
        return self.__map[x][y]
    
    def positions_of_type(self, cell_type : CellType) -> list:
        result : list = []
        for row in range(self.__rows):
            for column in range(self.__columns):
                cell : Cell = self.__map[row][column]
                if cell.cell_type == cell_type:
                    result.append((row, column))
        return result

    def find_valid_neighbour(self, cell : Cell) -> list:
        delta = [('W', (-1,0)), ('E', (1,0)), ('S', (0,1)), ('N', (0,-1))]
        neighbours = []
        for direction, (dx, dy) in delta:
            x2, y2 = cell.x + dx, cell.y + dy
            if (0 <= x2 < self.__rows) and (0 <= y2 < self.__columns):
                neighbour : Cell = self.cell_at(x2, y2)
                if neighbour.has_all_walls():
                    neighbours.append((direction, neighbour))
        return neighbours

    def to_adj_matrix(self) -> np.ndarray:
        cell_count : int = self.__rows * self.__columns + 1 + self.__enemy_count
        graph : np.ndarray = np.zeros((cell_count, cell_count), 'int')
        
        current_out_cell : int = self.__rows * self.__columns

        def set_adj_matrix(cell : Cell, cell_code : int):
            if cell.cell_walls['N'] and 0 <= cell.y - 1 < self.__columns and 0 <= cell.x < self.__rows:
                other : Cell = self.cell_at(cell.x, cell.y - 1)
                graph[cell_code][other.cell_code] = 1
            if cell.cell_walls['S'] and 0 <= cell.y + 1 < self.__columns and 0 <= cell.x < self.__rows:
                other : Cell = self.cell_at(cell.x, cell.y + 1)
                graph[cell_code][other.cell_code] = 1
            if cell.cell_walls['E'] and 0 <= cell.x + 1 < self.__rows and 0 <= cell.y < self.__columns:
                other : Cell = self.cell_at(cell.x + 1, cell.y)
                graph[cell_code][other.cell_code] = 1
            if cell.cell_walls['W'] and 0 <= cell.x - 1 < self.__rows and 0 <= cell.y < self.__columns:
                other : Cell = self.cell_at(cell.x - 1, cell.y)
                graph[cell_code][other.cell_code] = 1

        for row in range(self.__rows):
            for column in range(self.__columns):
                cell : Cell = self.cell_at(row, column)

                if cell.cell_type in [CellType.NONE, CellType.PLAYER, CellType.DOOR]:
                    set_adj_matrix(cell, cell.cell_code)

                    if cell.cell_type == CellType.PLAYER:
                        self.__player_cell_code = cell.cell_code
                    elif cell.cell_type == CellType.DOOR:
                        self.__door_cell_code = cell.cell_code

                elif cell.cell_type == CellType.KEY:
                    self.__key_mat_indexes = cell.cell_code, current_out_cell

                    graph[cell.cell_code][current_out_cell] = 1

                    set_adj_matrix(cell, current_out_cell)

                    current_out_cell += 1
                else:
                    enemy_indexes : tuple = cell.cell_code, current_out_cell
                    self.__enemies_mat_indexes.append(enemy_indexes)

                    graph[cell.cell_code][current_out_cell] = 0

                    set_adj_matrix(cell, current_out_cell)

                    current_out_cell += 1

        return graph

    def generate(self, start_x : int, start_y : int):
        n : int = self.__rows * self.__columns
        cell_stack : list = []
        current_cell : Cell = self.cell_at(start_x, start_y)
        visited_cells : int = 1
        while visited_cells < n:
            neighbours : list = self.find_valid_neighbour(current_cell)
            if not neighbours:
                current_cell = cell_stack.pop()
                continue
            direction, next_cell = random.choice(neighbours)
            current_cell.knock_down_wall(next_cell, direction)
            cell_stack.append(current_cell)
            current_cell = next_cell
            visited_cells += 1
        
        self.__adj_matrix = self.to_adj_matrix()

    def distance(self, a_id : int, b_id : int) -> int:
        distances : list = [inf] * len(self.__adj_matrix)
        last_node_in_path : list = [-1] * len(self.__adj_matrix)
        queue : list = list(range(len(self.__adj_matrix)))

        distances[a_id] = 0

        while len(queue) > 0:
            u : int = min(queue)
            queue.remove(u)
            for v in range(self.__adj_matrix[u]):
                if self.__adj_matrix[u][v] == 1:
                    if distances[v] > distances[u] + 1:
                        distances[v] = distances[u] + 1
                        last_node_in_path[v] = u
        
        return distances[b_id]

    def set_different_cell_types(self):
        used_cells : list = []
        enemy_type_list : list = [CellType.ENEMY_1, CellType.ENEMY_2, CellType.ENEMY_3]
        
        def pick_a_cell(cell_type : CellType):
            while True:
                row : int = random.choice(range(self.__rows))
                column : int = random.choice(range(self.__columns))

                if not (row, column) in used_cells:
                    used_cells.append((row, column))
                    self.cell_at(row, column).cell_type = cell_type
                    break

        for cell_type in [CellType.PLAYER, CellType.DOOR, CellType.KEY]:
            pick_a_cell(cell_type)
        
        for i in range(self.__enemy_count):
            pick_a_cell(random.choice(enemy_type_list))
