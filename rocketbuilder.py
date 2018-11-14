import pygame as pg
import pymunk as pm
import pymunk.pygame_util as pygame_util
import sys
import os
import math
from enum import Enum
from rockets import Component
from rockets import Thruster
from rockets import SAS
from rockets import Rocket

from graphics import Graphics

class RocketBuilder:

    surface = None
    componentSurface = None
    componentInfoSurface = None

    componentTabs = Enum("State", "Thruster Control Potato Famine")
    selectedTab = componentTabs.Thruster

    _bgColor = (0,0,0)
    _menuPaneColor = (128,128,128)
    _menuButtonColor = ((100,100,100),(64,64,64))  

    _bottomOfTabs = 0

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
        # fill with color
        cls.componentSurface.fill(cls._menuPaneColor)
        cls.drawComponentTabs()
        cls.drawComponentList(cls.selectedTab)

    @classmethod
    def drawComponentList(cls, selectedTab):
        buttonMargin = 10
        buttonSize = 100

        componentList = None

        if selectedTab == cls.componentTabs.Thruster:
            componentList = Thruster.__subclasses__()
        elif selectedTab == cls.componentTabs.Control:
            componentList = SAS.__subclasses__()              

        # find the number columns that can fit in the surface
        numCols = int((cls.componentSurface.get_width() + buttonMargin) / (buttonSize + buttonMargin))
        numRows = int(len(componentList) / numCols)
        if len(componentList) % numCols != 0:
            numRows += 1
        
        i = 0
        for component in componentList:
            pos = ((i % numCols) * buttonSize + buttonMargin, int(i / numCols) * buttonSize + cls._bottomOfTabs + buttonMargin)
            size = (buttonSize - buttonMargin, buttonSize - buttonMargin)

            Graphics.drawButton(cls.componentSurface, pos, size, cls._menuButtonColor, component._sprite, .95)

            i += 1

        

    @classmethod
    def drawComponentTabs(cls):
        font = pg.font.SysFont('Consolas', 16)
        buttonHeight = 40
        buttonTextMargin = 15

        # find the size of the text of each menu tab
        tabTexts = [str(component)[6:len(str(component))] for component in cls.componentTabs]
        buttonSizes = [font.size(text) for text in tabTexts]
        buttonSizes = [(x + 2*buttonTextMargin, y) for (x,y) in buttonSizes]
        buttonLines = [[]]


        # work out which string goes on which line
        currLine = 0
        for i in range(len(buttonSizes)):
            # find the width of this string
            width = buttonSizes[i][0]
            
            # find the width of the rest of this line
            lineWidth = 0
            for text in buttonLines[currLine]:
                lineWidth += text[0]

            if width + lineWidth < cls.componentSurface.get_width():
                buttonLines[currLine].append((buttonSizes[i][0], tabTexts[i]))
            else:
                currLine += 1
                buttonLines.append([(buttonSizes[i][0], tabTexts[i])])

        cls._bottomOfTabs = len(buttonLines) * buttonHeight

        for row in range(len(buttonLines)):
            width = int(cls.componentSurface.get_width() / len(buttonLines[row]))
            for col in range(len(buttonLines[row])):
                pos = (col * width, row * buttonHeight)
                size = None
                # now check if this is the rightmost button in a row
                # if so, need to extend it to dodge the integer division required earlier
                # from leaving a gap
                if col == len(buttonLines[row]) - 1:
                    size = (cls.componentSurface.get_width() - pos[0], buttonHeight)
                else:
                    size = (width, buttonHeight)
                Graphics.drawButton(cls.componentSurface, pos, size, cls._menuButtonColor, buttonLines[row][col][1], 16)

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
