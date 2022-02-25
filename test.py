import pygame as pg
import sys
 
sc = pg.display.set_mode((300, 200))
surf = pg.Surface((200, 150))
surf.fill((255, 255, 255))
sc.blit(surf, (50, 25))
pg.display.update()
 
while 1:
    for i in pg.event.get():
        if i.type == pg.QUIT:
            sys.exit()
    pg.time.delay(100)