import pygame as pg

import game
import rendering

app : game.Game = game.Game()

window = pg.display.set_mode((600, 400))
pg.display.set_caption('Just Another Zelda Clone')

test_obj : game.GameObject = game.GameObject(game.Transform((0, 0), 0))
test_obj.add_component(rendering.SpriteRenderer('assets/sprites/player_walk.png', 16, 16))

test_scene : game.Scene = game.Scene([test_obj])

app.add_scene(test_scene)

app.start()
app.update(window)
