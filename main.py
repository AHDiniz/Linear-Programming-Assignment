import pygame as pg

pg.init()

window = pg.display.set_mode((500, 400))

running = True

while running:
    pg.draw.rect(window, (255, 0, 0), (0, 0, 50, 30))

    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False

    pg.display.update()
