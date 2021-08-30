from game import Component
from game import GameObject
from game import Transform
from game import Time
import pygame as pg

class SpriteRenderer(Component):
    def __init__(self, sheet_path : str, sprite_width : int, sprite_height : int, sprite_scale : int = 1):
        self.__sheet_path = sheet_path
        self.__sprite_width = sprite_width
        self.__sprite_height = sprite_height
        self.__sprite_scale = sprite_scale
    
    def start(self):
        self.__sprite_sheet = pg.image.load(self.__sheet_path)
        self.__width = self.__sprite_sheet.get_width()
        self.__height = self.__sprite_sheet.get_height()
        self.__sprite_sheet = pg.transform.scale(self.__sprite_sheet, (self.__width * self.__sprite_scale, self.__height * self.__sprite_scale))
        self.__width, self.__height = self.__width * self.__sprite_scale, self.__height * self.__sprite_scale
        self.__rows = int(self.__height / self.__sprite_height)
        self.__columns = int(self.__width / self.__sprite_width)
        self.__sprite_rect = pg.Rect(0, 0, self.__sprite_width, self.__sprite_height)
    
    def update(self, surface : pg.Surface, game_object : GameObject):
        surface.blit(self.__sprite_sheet, game_object.position, self.__sprite_rect)

    def set_current_sprite(self, sprite_index : int):
        sprite_index = sprite_index % (self.__rows * self.__columns)
        target_row = int(sprite_index / self.__columns)
        target_column = int(sprite_index % self.__columns)
        self.__sprite_rect = pg.Rect(target_row * self.__sprite_width, target_column * self.__sprite_height, self.__sprite_width, self.__sprite_height)

class Animator(Component):
    def __init__(self, sprite_renderer : SpriteRenderer):
        self.__renderer : SpriteRenderer = sprite_renderer
        self.__sprite_index : int = 0
        self.__ms_to_change : int = 50
        self.__timer : int = 0
    
    def start(self):
        pass
    
    def update(self, surface : pg.Surface, game_object : GameObject):
        t : Time = Time()
        self.__timer += t.delta()
        if self.__timer >= self.__ms_to_change:
            print(self.__timer)
            self.__timer = 0
            self.__renderer.set_current_sprite(self.__sprite_index)
            self.__sprite_index += 1
