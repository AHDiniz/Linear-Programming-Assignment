import pygame as pg

class Transform:
    def __init__(self, p : tuple, r : float):
        self.__position = p
        self.__rotation = r
    
    def get_position(self) -> tuple:
        return self.__position
    
    def set_position(self, p : tuple):
        self.__position = p

    def get_rotation(self) -> float:
        return self.__rotation
    
    def set_rotation(self, r : float):
        self.__rotation = r
    
    rotation = property(get_rotation, set_rotation)
    position = property(get_position, set_position)

class GameObject:
    def __init__(self, transform : Transform):
        self.__components = list([])
        self.__transform = transform

    @property
    def transform(self) -> Transform:
        return self.__transform
    
    @property
    def position(self) -> tuple:
        return self.__transform.position
    
    @property
    def rotation(self) -> float:
        return self.__transform.rotation
    
    def start(self):
        for component in self.__components:
            component.start()
    
    def update(self, surface : pg.Surface):
        for component in self.__components:
            component.update(surface)

    def add_component(self, component):
        component.set_parent(self)
        self.__components.append(component)

class Component:
    def __init__(self):
        pass

    @property
    def game_object(self) -> GameObject:
        return self.__game_object

    def start(self):
        pass
    
    def update(self, surface : pg.Surface):
        pass
    
    def set_parent(self, go : GameObject):
        self.__game_object = go

class Scene:
    def __init__(self, game_objects : list):
        self.__game_objects = game_objects

    def start(self):
        for go in self.__game_objects:
            go.start()

    def update(self, surface : pg.Surface):
        for go in self.__game_objects:
            go.update(surface)

class Game:
    def __init__(self):
        pg.init()
        self.__running = True
        self.__scenes = list([])
        self.__current_scene = 0

    def start(self):
        self.__scenes[self.__current_scene].start()
    
    def update(self, window):
        while self.__running:
            self.__scenes[self.__current_scene].update(window)

            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.__running = False

            pg.display.update()
    
    def add_scene(self, scene : Scene):
        self.__scenes.append(scene)

    def change_scene(self, scene_index : int):
        self.__current_scene = scene_index
        self.__scenes[self.__current_scene].start()