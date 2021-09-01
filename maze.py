class Cell:
    wall_pairs = {'N' : 'S', 'S' : 'N', 'E' : 'W', 'W' : 'E'}

    def __init__(self, x : int, y : int):
        self.__x, self.__y = x, y
        self.__walls = ['N': True, 'S': True, 'E': True, 'W': True]
    
    @property
    def x(self):
        return self.__x
    
    @property
    def y(self):
        return self.__y

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
                self.__map[i].append(Cell(i, j))
    
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

    def generate(start_x : int, start_y : int):
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
