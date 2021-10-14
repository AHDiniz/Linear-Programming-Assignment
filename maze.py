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
    
    @property
    def neighbour_count(self) -> int:
        result : int = 0
        for _, value in self.__walls.items():
            if value:
                result += 1
        return result
    
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

    @property
    def dimensions(self) -> tuple:
        return (self.__rows, self.__columns)

    def cell_at(self, x : int, y : int) -> Cell:
        return self.__map[x][y]
    
    def cell_with_code(self, code : int) -> Cell:
        x : int = int(code / self.__rows)
        y : int = code % self.__columns
        return self.cell_at(x, y) 

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

    def find_bifurcations(self) -> list:
        result : list = []
        for row in self.__map:
            for cell in row:
                neighbours : list = self.get_neighbours(cell)
                if len(neighbours) > 2:
                    result.append(cell)
        return result

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

    def get_neighbours(self, cell : Cell) -> list:
            neighbours : list = []
            if not cell.cell_walls['N']:
                neighbours.append(self.cell_at(cell.x, cell.y - 1))
            if not cell.cell_walls['E']:
                neighbours.append(self.cell_at(cell.x + 1, cell.y))
            if not cell.cell_walls['S']:
                neighbours.append(self.cell_at(cell.x, cell.y + 1))
            if not cell.cell_walls['W']:
                neighbours.append(self.cell_at(cell.x - 1, cell.y))
            return neighbours

    def define_reduction_data(self) -> list:
        visited_cells : list = [False] * (self.__rows * self.__columns)
        player_pos : tuple = (self.positions_of_type(CellType.PLAYER))[0]
        player : Cell = self.cell_at(player_pos[0], player_pos[1])

        paths : list = []

        def recursion(cell : Cell, path : list):
            visited_cells[cell.cell_code] = True
            neighbours : list = self.get_neighbours(cell)
            neighbours_count : int = len(neighbours)
            visited_neighbours_list : list = list(filter(lambda x: visited_cells[x.cell_code], neighbours))
            visited_neighbours : int = len(visited_neighbours_list)
            if neighbours_count == 1 or neighbours_count == visited_neighbours:
                path.append(cell)
                paths.append(path)
            elif cell.cell_type == CellType.NONE and neighbours_count - visited_neighbours == 1:
                path.append(cell)
                for n in neighbours:
                    if not visited_cells[n.cell_code]:
                        recursion(n, path)
            else:
                path.append(cell)
                paths.append(path)
                for n in neighbours:
                    if not visited_cells[n.cell_code]:
                        recursion(n, [cell])

        recursion(player, [])

        return paths

    # Returns adjacency matrix and dictionary of cell codes and matrix indices:
    def to_reduced_adj_matrix(self) -> tuple:
        paths : list = self.define_reduction_data()
        reverse_paths : list = []

        nodes : list = []
        edges : dict = {}

        index_dict : dict = {}
        matrix_size : int = len(paths) + 1 + self.__enemy_count
        adj_matrix : np.ndarray = np.zeros((matrix_size, matrix_size))

        for path in paths:
            reverse_path : list = path.copy()
            reverse_path.reverse()
            reverse_paths.append(reverse_path)
        
        for reverse_path in reverse_paths:
            paths.append(reverse_path)

        for path in paths:
            if len(path) == 1:
                continue

            start : Cell = path[0]
            end : Cell = path[-1]

            if not start in nodes:
                nodes.append(start)
            
            if not end in nodes:
                nodes.append(end)
            
            if start.cell_type in [CellType.KEY, CellType.ENEMY_1, CellType.ENEMY_2, CellType.ENEMY_3]:
                edges[(-start.cell_code, end.cell_code)] = len(path)
                edges[(start.cell_code, -start.cell_code)] = 1
            else:
                edges[(start.cell_code, end.cell_code)] = len(path)
            
            if start.cell_type == CellType.KEY:
                self.__key_mat_indexes = start.cell_code, end.cell_code
                

        for node in nodes:
            index_dict[node.cell_code] = -1
            if node.cell_type in [CellType.KEY, CellType.ENEMY_1, CellType.ENEMY_2, CellType.ENEMY_3]:
                index_dict[-node.cell_code] = -1
                
        
        current_index : int = 0
        for edge, capacity in edges.items():
            start : int = edge[0]
            end : int = edge[1]

            if index_dict[start] == -1:
                index_dict[start] = current_index
                current_index += 1
            
            if index_dict[end] == -1:
                index_dict[end] = current_index
                current_index += 1

            adj_matrix[index_dict[start]][index_dict[end]] = capacity
        
        return adj_matrix, index_dict

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
