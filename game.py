import pygame as pg
import time
import os
import sys
import asyncio

class GooseGame:
    def __init__(self):
        os.environ['SDL_VIDEO_CENTERED'] = "1"
        pg.init()
        self.screen = pg.display.set_mode((800, 600)) # add parameter, pg.FULLSCREEN when finished
        pg.display.set_caption("Goose Game")
        self.clock = pg.time.Clock()

    def quit(self):
            pg.quit()
            #sys.exit()

    async def run_gui(self):
        self.screen.blit(self.screen, (0,0))
        current_color = (255,255,255)
        my_rect = pg.draw.rect(self.screen, current_color, (50,50,50,50))
        while True:
            pg.display.update()
            for event in pg.event.get():
                if event.type == pg.MOUSEBUTTONDOWN:
                    mouse = pg.mouse.get_pos()
                    if my_rect.collidepoint(mouse):
                        current_color = (255,0,0)
                    else:
                        current_color = (0,255,0)
                    self.screen.fill((255,255,255))
                    my_rect = pg.draw.rect(self.screen, current_color, (50,50,50,50))
                if event.type == pg.QUIT:
                    self.quit()
            self.clock.tick(60)
            await asyncio.sleep(0)