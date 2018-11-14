import pygame as pg
import pymunk as pm
import pymunk.pygame_util as pygame_util
import sys
import os
import math
from pymunk import Poly as Poly
from pymunk import Body as Body
from pymunk import Shape as Shape


from enum import Enum
from rockets import Component
from rockets import Thruster
from rockets import SAS
from rockets import Rocket
from rockets import commandmodule

from graphics import Graphics

class RocketBuilder:

    surface = None
    componentSurface = None
    componentInfoSurface = None

    componentTabs = Enum("State", "Thruster Control Potato Famine")
    selectedTab = componentTabs.Thruster
    
    theRocket = Rocket([])
    _bgColor = (0,0,0)
    _menuPaneColor = (128,128,128)
    _menuButtonColor = ((100,100,100),(64,64,64))  

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
        # as a quick test, fill with color
        cls.componentSurface.fill(cls._menuPaneColor)

        font = pg.font.SysFont('Consolas', 16)

        # find the size of the text of each menu tab
        tabTexts = [str(component)[6:len(str(component))] for component in cls.componentTabs]
        buttonSizes = [font.size(text) for text in tabTexts]
        buttonLines = [[]]

        buttonHeight = 40

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

        for row in range(len(buttonLines)):
            width = int(cls.componentSurface.get_width() / len(buttonLines[row]))
            for col in range(len(buttonLines[row])):
                pos = (col * width, row * buttonHeight)
                size = (width, buttonHeight)
                Graphics.drawButton(cls.componentSurface, pos, size, cls._menuButtonColor, buttonLines[row][col][1], 16)

        
        # testImage = pg.image.load(os.path.join("assets", "sprites", "orbiter.png")).convert_alpha()
        # Graphics.drawButton(cls.componentSurface, (10,10), (100,100), ((64,64,64), (32,32,32)), testImage, .9)

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
    

    @classmethod
    def placeComponenet(cls, transform, component):
        #if it's intersecting/directly adjacent to another component on the rocket
        if intersectsWithRocket(component)
        return True
        #if it's not return false, but thats a #TODO for later
        cls.theRocket.addComponent(component) #add the component to the rocket
        #TODO provide offset to add component at, will just add at the specified offset native to vertices for now

    @classmethod
    def removeComponent(cls, component):
        cls.theRocket.removeComponent(component)
   
    
    @classmethod
    def intersectsWithRocket(cls, component):
        verts = component.get_vertices()
        totalverts = len(verts)
        intersects = False
        for x in range(totalverts)
            if x == 0:
                verts1 = verts[0]
                verts2 = verts[totalverts -1]
            else:
                verts1 = verts[x]
                verts2 = verts[x-1]
            for i in Rocket.shapes:
                if i.segment_query(verts1, verts2, 1).shape != None :
                    intersects = True
                    break
            if intersects == True:
                    break
        return intersects