import pygame as pg
import pymunk as pm
import pymunk.pygame_util as pygame_util
import sys
import os
import math
from rockets import Component
from rockets import Thruster
from rockets import SAS
from rockets import Rocket

from graphics import Graphics

class RocketBuilder:

    surface = None
    componentSurface = None
    componentInfoSurface = None

    _bgColor = (0,0,0)
    _menuPaneColor = (128,128,128)    

    @classmethod
    def run(cls):
        # while loop to draw infinitely for testing purposes
        clock = pg.time.Clock()     # create clock to manage game time
        cls.updateSubSurfaces()
        while True:                 # drawn menu infinitely
            cls.drawMenu()
            for event in pg.event.get():
                if event.type == pg.VIDEORESIZE:
                    cls.surface = pg.display.set_mode((event.w, event.h), pg.RESIZABLE)
                    cls.updateSubSurfaces()
                if event.type == pg.QUIT:
                    pg.display.quit()
                    pg.quit()
                    sys.exit()
            clock.tick(60)
            
    @classmethod
    def drawMenu(cls):
        cls.surface.fill(cls._bgColor)
        cls.drawComponentMenu()
        cls.drawComponentInfo()
        pg.display.flip()

    @classmethod
    def drawComponentMenu(cls):
        # as a quick test, fill with white
        cls.componentSurface.fill(cls._menuPaneColor)
        testImage = pg.image.load(os.path.join("assets", "sprites", "orbiter.png")).convert_alpha()
        Graphics.drawButton(cls.componentSurface, (10,10), (100,100), ((64,64,64), (32,32,32)), testImage, .9)

    @classmethod
    def drawComponentInfo(cls):
        # as a quick test, fill with white
        cls.componentInfoSurface.fill(cls._menuPaneColor)

    @classmethod
    def updateSubSurfaces(cls):
        cls.surface = pg.display.get_surface()
        cls.componentSurface = cls.surface.subsurface(
            pg.Rect(
                (0,0),   # top-left corner of screen
                (cls.surface.get_size()[0]/4, cls.surface.get_size()[1]) # left 1/4 of screen
            ))

        cls.componentInfoSurface = cls.surface.subsurface(
            pg.Rect(
                (3*cls.surface.get_size()[0]/4, 0),  # origin of right 1/4 of screen
                (cls.surface.get_size()[0]/4, cls.surface.get_size()[1]) # right 1/4 of screen
            ))
