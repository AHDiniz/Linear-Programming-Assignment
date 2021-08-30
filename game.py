import pygame as pg

MS_PER_UPDATE : int = 17

class Time:
    delta_time = 0

    @classmethod
    def set_delta(self, d : int):
        self.delta_time = d
    
    @classmethod
    def delta(self):
        return self.delta_time

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
            component.update(surface, self)

    def add_component(self, component):
        self.__components.append(component)

class Component:
    def __init__(self):
        pass

    @property
    def game_object(self) -> GameObject:
        return self.__game_object

    def start(self):
        pass
    
    def update(self, surface : pg.Surface, game_object : GameObject):
        pass

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
        prev : float = pg.time.get_ticks()
        lag : float = 0

        t : Time = Time()

        while self.__running:
            current : float = pg.time.get_ticks()
            delta = current - prev
            prev = current
            lag += delta

            t.set_delta(delta)

            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.__running = False

            while lag >= MS_PER_UPDATE:
                self.__scenes[self.__current_scene].update(window)
                lag -= MS_PER_UPDATE

            pg.display.update()
    
    def add_scene(self, scene : Scene):
        self.__scenes.append(scene)

    def change_scene(self, scene_index : int):
        self.__current_scene = scene_index
        self.__scenes[self.__current_scene].start()