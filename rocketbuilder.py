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
from rockets import CommandModule

from graphics import Drawer
from graphics import Graphics

class RocketBuilder:

    surface = None
    componentSurface = None
    componentInfoSurface = None

    componentTabs = Enum("State", "Thruster Control Potato Famine")
    componentList = []
    selectedTab = componentTabs.Thruster
    
    theRocket = Rocket([CommandModule(None)])

    activeComponent = None
    activeSprite = None
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
            pos = pg.mouse.get_pos()
            if cls.activeSprite != None :
                cls.activeSprite.set_rect(pos)
             
            for event in pg.event.get():
                if event.type == pg.VIDEORESIZE:
                    cls.surface = pg.display.set_mode((event.w, event.h), pg.RESIZABLE)
                    cls.updateSubSurfaces()
                if event.type == pg.QUIT:
                    pg.display.quit()
                    pg.quit()
                    sys.exit()
                if event.type == pg.MOUSEBUTTONUP :
                    
                    if cls.activeComponent == None : #not "holding" anything
                        sprite_list = []
                        for s in cls.componentList :
                            sprite_list.append(s._sprite)
                        clicked_sprites = [s for s in sprite_list if s.get_rect().collidepoint(pos)]
                        
                        for s in clicked_sprites :
                            print("activated")
                            target_index = clicked_sprites.index(s)
                            cls.activeComponent = cls.componentList[target_index]
                            cls.activeSprite = s
                    else:
                        cls.placeComponenet(pm.Transform(tx=0, ty=0), cls.activeComponent)
                        cls.activeComponent = None
                        cls.activeSprite = None
                
            clock.tick(60)
            
    @classmethod
    def drawMenu(cls):
        cls.surface.fill(cls._bgColor)
        cls.drawComponentMenu()
        cls.drawComponentInfo()
        cls.drawRocket()
        cls.drawHeldSprite()
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

        cls.componentList = None

        if selectedTab == cls.componentTabs.Thruster:
            cls.componentList = Thruster.__subclasses__()
        elif selectedTab == cls.componentTabs.Control:
            cls.componentList = SAS.__subclasses__()              

        # find the number columns that can fit in the surface
        numCols = int((cls.componentSurface.get_width() + buttonMargin) / (buttonSize + buttonMargin))
        numRows = int(len(cls.componentList) / numCols)
        if len(cls.componentList) % numCols != 0:
            numRows += 1
        
        i = 0
        for component in cls.componentList:
            pos = ((i % numCols) * buttonSize + buttonMargin, int(i / numCols) * buttonSize + cls._bottomOfTabs + buttonMargin)
            size = (buttonSize - buttonMargin, buttonSize - buttonMargin)

            Graphics.drawButton(cls.componentSurface, pos, size, cls._menuButtonColor, component._sprite, .95, lambda: cls.componentButtonClicked(component))

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
    def drawRocket(cls):
        Drawer.drawMultiple(cls.surface, cls.theRocket.components,
                            Drawer.getOffset(cls.surface, cls.theRocket))

    @classmethod
    def drawHeldSprite(cls):
        if cls.activeComponent is not None:
            mouse_x, mouse_y = pg.mouse.get_pos()
            pos = (mouse_x - cls.activeComponent._sprite.get_width()/2, mouse_y - cls.activeComponent._sprite.get_height()/2)
            cls.surface.blit(cls.activeComponent._sprite, pos)

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
        if cls.intersectsWithRocket(component) :
            transform = cls.mousePosToPymunkTransform(pg.mouse.get_pos(), component)
            cls.theRocket.addComponent(component(body=None, transform=transform))
            return True
        else:
            return False
        
    @classmethod
    def mousePosToPymunkTransform(cls, mousePos, component):
        """Takes in a component class or instance, and the mouse position. Assuming
           that the component is being held by mouse in its center, this finds the
           transform needed to translate between the component's inherent verteces
           and the mouse's current position in pymunk space.

            Args:
                mousePos (int, int): mouse's position to translate
                component (component): the component who's verticies to translate

        """
        # pull in component boundaries
        minX, maxX, minY, maxY = Component.getXYBoundingBox(component._vertices)

        # find the geometric center of the component, which is flipped in the y
        # direction because of pygame's different y axis
        componentCenter = pm.Vec2d((minX + maxX) / 2, (minY + maxY) / -2)

        # finding center of the screen
        screenCenter = pm.Vec2d(cls.surface.get_size())/2

        # vector to the center of the screen in pygame pixels
        dx, dy = (mousePos - screenCenter) - componentCenter

        # flip dy between pymunk coordinates and pymunk screen-space coordinates
        dy *= -1

        return pm.Transform(tx=dx, ty=dy)

    @classmethod
    def removeComponent(cls, component):
        cls.theRocket.removeComponent(component)
   
    
    @classmethod
    def intersectsWithRocket(cls, component):
        # create a list of updated vertices, accounting for current mouse position
        vertices = []
        transform = cls.mousePosToPymunkTransform(pg.mouse.get_pos(), component)
        for vertex in component._vertices:
            vertices.append(pm.Vec2d(vertex) + (transform.tx, transform.ty))

        totalverts = len(vertices)

        for x in range(totalverts):
            if x == 0:
                verts1 = vertices[0]
                verts2 = vertices[totalverts - 1]
            else:
                verts1 = vertices[x]
                verts2 = vertices[x-1]
            for comp in cls.theRocket.components:
                if comp.segment_query(verts1, verts2, 1).shape != None :
                    return True

        return False

    @classmethod
    def componentButtonClicked(cls, component) :
        cls.activeComponent = component
