from game import Component
from game import GameObject
from game import Transform
import pygame as pg

class SpriteRenderer(Component):
    def __init__(self, sheet_path : str, sprite_width : int, sprite_height : int):
        self.__sheet_path = sheet_path
        self.__sprite_width = sprite_width
        self.__sprite_height = sprite_height
    
    def start(self):
        self.__position : tuple = Component.game_object.position
        self.__sprite_sheet = pg.image.load(self.__sheet_path)
        self.__width = self.__sprite_sheet.get_width()
        self.__height = self.__sprite_sheet.get_height()
        self.__rows = int(self.__height / self.__sprite_height)
        self.__columns = int(self.__width / self.__sprite_width)
        self.__sprite_rect = (0, 0, self.__sprite_width, self.__sprite_height)
    
    def update(self, surface : pg.Surface):
        surface.blit(self.__sprite_sheet, self.__position, self.__sprite_rect)

    def set_current_sprite(self, sprite_index : int):
        sprite_index = sprite_index % (self.__rows * self.__columns)
        target_row = int(sprite_index / self.__columns)
        target_column = int(sprite_index % self.__columns)
        self.__sprite_rect.move(target_row * self.__sprite_width, target_column * self.__sprite_height)
