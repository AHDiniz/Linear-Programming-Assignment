from enum import Enum

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
        self.__x : int, self.__y : int = x, y
        self.__walls : dict = ['N': True, 'S': True, 'E': True, 'W': True]
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
    
    def knock_down_wall(self, other : Cell, wall : str):
        self.__walls[wall] = False
        other.__walls[Cell.wall_pairs[wall]] = False

class Maze:
    def __init__(self, width : int, height : int, tile_types : list):
        self.__width : int = width
        self.__height : int = height
        self.__tile_types : list = tile_types
        self.__map : list = list([])

        for i in range(self.__height):
            self.__map.append(list([]))
            for j in range(self.__width):
                self.__map[i].append(Cell(i * self.__height + j, i, j, CellType.NONE))
    
    def cell_at(self, x : int, y : int) -> Cell:
        return self.__map[x][y]

    def find_valid_neighbour(self, cell : Cell) -> list:
        delta = [('W', (-1,0)), ('E', (1,0)), ('S', (0,1)), ('N', (0,-1))]
        neighbours = []
        for direction, (dx, dy) in delta:
            x2, y2 = cell.x + dx, cell.y + dy
            if (0 <= x2 < self.__width) and (0 <= y2 < self.__height):
                neighbour : Cell = self.cell_at(x2, y2)
                if neighbour.has_all_walls():
                    neighbours.append((direction, neighbour))
        return neighbours

    def to_adj_matrix(self) -> list:
        graph : list = list([])
        for i in range(self.__height):
            graph.append([])
            for j in range(self.__width):
                graph[i].append(0)
        
        for row in range(self.__height):
            for column in range(self.__width):
                cell : Cell = self.cell_at(row, column)
                if cell.walls['N']:
                    graph[cell.cell_code][self.cell_at(cell.x, cell.y - 1).cell_code] = 1
                if cell.walls['S']:
                    graph[cell.cell_code][self.cell_at(cell.x, cell.y + 1).cell_code] = 1
                if cell.walls['E']:
                    graph[cell.cell_code][self.cell_at(cell.x + 1, cell.y).cell_code] = 1
                if cell.walls['W']:
                    graph[cell.cell_code][self.cell_at(cell.x - 1, cell.y).cell_code] = 1

        return graph

    def generate(self, start_x : int, start_y : int):
        n : int = self.__width * self.__height
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
