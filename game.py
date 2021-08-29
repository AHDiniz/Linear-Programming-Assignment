import pygame as pg

class Component:
    def __init__(self):
        pass
    
    def start(self):
        pass
    
    def update(self):
        pass

class GameObject:
    def __init__(self):
        self.components = list([])
        pass
    
    def start(self):
        for component in self.components:
            component.start()
    
    def update(self):
        for component in self.components:
            component.update()

    def add_component(self, component : Component):
        self.components.add(component)

class Scene:
    def __init__(self, game_objects : list):
        self.game_objects = game_objects

    def start(self):
        for go in self.game_objects:
            go.start()

    def update(self):
        for go in self.game_objects:
            go.update()

class Game:
    def __init__(self):
        pg.init()
        self.running = True
        self.scenes = list([])

    def start(self):
        pass
    
    def update(self, window):
        while self.running:
            pg.draw.rect(window, (255, 0, 0), (0, 0, 50, 50))

            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.running = False

            pg.display.update()
    
    def add_scene(self, scene : Scene):
        self.scenes.add(scene)