import pygame as pg
import game

app : game.Game = game.Game()

window = pg.display.set_mode((600, 400))
pg.display.set_caption('Just Another Zelda Clone')

app.start()
app.update(window)
