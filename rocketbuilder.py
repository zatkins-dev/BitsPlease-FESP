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
from rockets import Thruster, SolidThruster, LiquidThruster, RCSThruster
from rockets import SAS
from rockets import Rocket
from rockets import Tank
from rockets import CommandModule

from graphics import Drawer
from graphics import Graphics

class RocketBuilder:
    """
    Gets component information and facilitates the construction of a new and
    unique :py:class:`rockets.rocket.Rocket` to use in the simulation
    """
    #: The :py:class:`pygame.surface.Surface` that the builder will be drawn to
    surface = None

    #: The Sub-Surface representing the :py:class:`pygame.surface.Surface` selection screen
    componentSurface = None
    #: The Sub-Surface representing the component information display
    componentInfoSurface = None

    #: A custom event for triggering the exit of the building step
    #: and the beginning of the simulation
    start_event = pg.USEREVENT + 1

    #: The :py:class:`pymunk.Space` used to construct the rocket
    space = pm.Space(threaded=True)
    space.threads = 2

    componentTabs = Enum("State", "Thruster Control Tanks")
    componentList = []
    #: The active category of components from componentTabs
    #: Initialized to the Thruster category
    selectedTab = componentTabs.Thruster
    
    #: This component will be the base, and can't be removed from the rocket in construction
    _baseComponent = CommandModule(None)

    #: The rocket being constructed
    theRocket = Rocket([_baseComponent])

    #: Used to represent the component that is being held by the user's mouse
    activeComponent = None

    #: The background color of the builder
    _bgColor = (0,0,0)
    #: The color of the menu panes
    _menuPaneColor = (128,128,128)
    #: The unfocused and focused colors of the menu buttons, respectively.
    _menuButtonColor = ((100,100,100),(64,64,64))  

    #: Represents the y position seperating the component category tabs
    #: from the actual buttons in the menu
    _bottomOfTabs = 0

    #: Represents whether components will be placed with symmetry about
    #: the center of the rocket
    _symmetry = False

    @classmethod
    def run(cls):
        """
        Contains and executes the main event loop of the rocket builder.
        """
        
        clock = pg.time.Clock()     # create clock to manage game time
        cls.theRocket.reset()
        if not cls.theRocket.components:
            cls.theRocket.components.append(cls._baseComponent)
        cls.space.add(cls.theRocket)
        cls.updateSubSurfaces()
        while True:                 # drawn menu infinitely
            cls.drawMenu()
            pos = pg.mouse.get_pos()
             
            for event in pg.event.get():
                if event.type == pg.VIDEORESIZE:
                    cls.surface = pg.display.set_mode((event.w, event.h), pg.RESIZABLE)
                    cls.updateSubSurfaces()
                if event.type == pg.QUIT:
                    pg.display.quit()
                    pg.quit()
                    sys.exit()
                if event.type is pg.MOUSEBUTTONDOWN:
                    if cls.activeComponent is None:
                        # no component in hand, so try to pick one up if possible

                        # find the position of the mouse in our space
                        screenCenter = pm.Vec2d(cls.surface.get_size())/2
                        mousePos = pm.pygame_util.get_mouse_pos(cls.surface) - screenCenter

                        # check every component in the list from back-to-front
                        # the last items in the component list will render on top,
                        # so this feels more natural to pick up
                        for component in reversed(cls.theRocket.components):
                            component.cache_bb()
                            # check if the mosue is within the component geometry
                            if component is not cls._baseComponent and component.point_query(mousePos)[0] <= 0:
                                # if so, set this as the shape and remove it
                                cls.activeComponent = type(component)
                                cls.theRocket.removeComponent(component)
                                break
                    if event.button == 4:
                        Drawer.zoom.zoom_out()
                    elif event.button == 5:
                        Drawer.zoom.zoom_in()
                if event.type == pg.MOUSEBUTTONUP :
                    if cls.activeComponent is not None:
                        cls.placeComponenet(cls.activeComponent)
                        cls.activeComponent = None
                if event.type == cls.start_event:
                    cls.space.remove(cls.theRocket)
                    return cls.theRocket
                
            clock.tick(60)
            
    @classmethod
    def drawMenu(cls):
        """
        Method encapsulates drawing of the entire rocket builder display,
        making this the top-level drawing method.
        """
        cls.surface.fill(cls._bgColor)
        cls.drawComponentMenu()
        cls.drawComponentInfo()
        cls.drawRocket()
        cls.drawHeldSprite()
        pg.display.flip()

    @classmethod
    def drawComponentMenu(cls):
        """
        Draws the component menu to the componentSurface class member, including
        the componentTabs and the componentList.
        """
        cls.componentSurface.fill(cls._menuPaneColor)
        cls.drawComponentTabs()
        cls.drawComponentList(cls.selectedTab)

    @classmethod
    def drawComponentList(cls, selectedTab):
        """
        Draws the list of available components to the screen using the provided category.
        
        :param enum.Enum selectedTab: The currently selected category of components to draw
        """
        buttonMargin = 10
        buttonSize = 100

        cls.componentList = None

        if selectedTab == cls.componentTabs.Thruster:
            cls.componentList = [thruster for thruster in SolidThruster.__subclasses__() + LiquidThruster.__subclasses__() + RCSThruster.__subclasses__()]
        elif selectedTab == cls.componentTabs.Control:
            cls.componentList = SAS.__subclasses__()  
        elif selectedTab == cls.componentTabs.Tanks:
            cls.componentList = Tank.__subclasses__()

        # find the number columns that can fit in the surface
        numCols = int((cls.componentSurface.get_width() + buttonMargin) / (buttonSize + buttonMargin))
        numRows = int(len(cls.componentList) / numCols)
        if len(cls.componentList) % numCols != 0:
            numRows += 1
        
        i = 0
        for component in cls.componentList:
            pos = ((i % numCols) * buttonSize + buttonMargin, int(i / numCols) * buttonSize + cls._bottomOfTabs + buttonMargin)
            size = (buttonSize - buttonMargin, buttonSize - buttonMargin)
            
            Graphics.drawButton(cls.componentSurface, pos, size, cls._menuButtonColor, Drawer.scaleSpriteToVerts(component._sprite, component.getInfo()["vertices"]), .8, lambda: cls.componentButtonClicked(component))

            i += 1

    @classmethod
    def drawComponentTabs(cls):
        """
        Draws the categorical tabs at the top of the componentSurface.
        """
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
                Graphics.drawButton(cls.componentSurface, pos, size, cls._menuButtonColor, buttonLines[row][col][1], 16, lambda: cls.setCurrentTab(cls.componentTabs[buttonLines[row][col][1]]))

    @classmethod
    def drawComponentInfo(cls):
        """
        Uses the active component to draw component information to the right info pane on the screen.
        """
        # fill with background color
        cls.componentInfoSurface.fill(cls._menuPaneColor)

        if cls.activeComponent is not None:
            # find the size & mass of the component
            globalAttributes = ["Width: ", "Height: ", "Mass: "]
            
            testComponent = cls.activeComponent(cls.theRocket)
            cls.space.add(testComponent)
            bb = testComponent.cache_bb()

            # find the geometric center of the component
            globalAttributes[0] += str(bb.right - bb.left) + "m"
            globalAttributes[1] += str(bb.top - bb.bottom) + "m"
            globalAttributes[2] += str(round(testComponent.mass, 1)) + "kg"

            cls.space.remove(testComponent)

            # print the values to the side

            nameFont = pg.font.SysFont("lucidaconsole", 24, True)
            attributeFont = pg.font.SysFont("lucidaconsole", 14)
            rowHeight = 24
            margin = 10

            textPos = lambda rowNum: (margin, rowHeight * rowNum + margin)

            Graphics.drawText(textPos(0), cls.activeComponent.__name__, nameFont, surface=cls.componentInfoSurface)

            currRow = 1

            for attribute in globalAttributes:
                Graphics.drawText(textPos(currRow), attribute, attributeFont, surface=cls.componentInfoSurface)
                currRow += 1
            
            dispInfo = cls.activeComponent.getDisplayInfo()
            for key in dispInfo:
                Graphics.drawText(textPos(currRow), key + ": " + str(dispInfo[key]), attributeFont, surface=cls.componentInfoSurface)
                currRow += 1
        
        # draw a start button in the corner
        buttonMargin = cls.componentInfoSurface.get_width() * .05
        startButtonSize = (cls.componentInfoSurface.get_width() - 2 * buttonMargin, 80)
        startButtonPos = (buttonMargin, cls.componentInfoSurface.get_height() - 80 - buttonMargin)
        startButtonColor = ((0,200,0),(0,100,0))
        Graphics.drawButton(cls.componentInfoSurface, startButtonPos, startButtonSize, startButtonColor, "Start", 16, lambda: pg.event.post(pg.event.Event(cls.start_event)))

        # draw a toggle symmetry button
        symButtonSize = startButtonSize
        symButtonPos = startButtonPos[0], startButtonPos[1] - buttonMargin - symButtonSize[1]
        symButtonColor = ((150,150,150), (100,100,100))
        symText = "Symmetry:  On" if cls._symmetry else "Symmetry: Off"
        Graphics.drawButton(cls.componentInfoSurface, symButtonPos, symButtonSize, symButtonColor, symText, 16, cls.toggleSymmetry)

    @classmethod
    def drawRocket(cls):
        """
        Draws the rocket-in-construction to the center of the display surface.
        """
        Drawer.drawMultiple(cls.surface, cls.theRocket.components,
                            Drawer.getOffset(cls.surface, cls.theRocket))

    @classmethod
    def drawHeldSprite(cls):
        """
        Draws the sprite of the active component to the screen at the position of the mouse
        """
        if cls.activeComponent is not None:
            # create a test component at the mouse position
            testComp = cls.activeComponent(None, transform=cls.mousePosToPymunkTransform(cls.activeComponent))
            # give add the component to the rocket (and space)
            cls.theRocket.addComponent(testComp)
            # draw the part at this location...
            Drawer.draw(cls.surface, testComp, Drawer.getOffset(cls.surface, cls.theRocket))
            # then remove it.
            cls.theRocket.removeComponent(testComp)

    @classmethod
    def updateSubSurfaces(cls):
        """
        A helper method the correctly set the size and position of the componentSurface and componentInfoSurface
        when the game window is resized.
        """
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
    def placeComponenet(cls, component):
        """
        Tests if it is possible to place the given component, and will place it if possible.
        Returns True if the component was placed, and False if it was not.
        
        :param rockets.Component component: The component to attempt to place
        """
        #if it's intersecting/directly adjacent to another component on the rocket
        if cls.intersectsWithRocket(component) :
            transform = cls.mousePosToPymunkTransform(component)
            cls.theRocket.addComponent(component(body=None, transform=transform))
            if cls._symmetry:
                symTransform = cls.mousePosToPymunkTransform(component, True)
                cls.theRocket.addComponent(component(body=None, transform=symTransform))

            return True
        else:
            return False
        
    @classmethod
    def mousePosToPymunkTransform(cls, component, reflected=False):
        """
        Takes in a component class or instance, and the mouse position. Assuming
        that the component is being held by mouse in its center, this finds the
        transform needed to translate between the component's inherent verteces
        and the mouse's current position in pymunk space.

        :param rockets.Component component: The component who's position to transform
        :param Bool reflected: Will reflect the transform about the x axis if set to True
        """
        # pull in component boundaries
        #minX, maxX, minY, maxY = Component.getXYBoundingBox(component._vertices)
        testComponent = component(cls.theRocket)
        cls.space.add(testComponent)
        bb = testComponent.cache_bb()

        # find the geometric center of the component
        componentCenter = bb.center()

        cls.space.remove(testComponent)

        # finding center of the screen
        screenCenter = pm.Vec2d(cls.surface.get_size())/2

        # finding the mouse position, in pymunk space
        mousePos = pm.pygame_util.get_mouse_pos(cls.surface)
        if reflected:
            mousePosX, mousePosY = pm.pygame_util.get_mouse_pos(cls.surface)
            mousePos = cls.surface.get_width() - mousePosX, mousePosY

        # vector to the center of the screen in pygame pixels
        dx, dy = (mousePos - screenCenter) - componentCenter

        # flip dy between pymunk coordinates and pymunk screen-space coordinates

        return pm.Transform(tx=dx, ty=dy)

    @classmethod
    def removeComponent(cls, component):
        """
        Removes a component from the rocket.

        :param rockets.Component component: The component to attempt to remove
        """
        cls.theRocket.removeComponent(component)
   
    
    @classmethod
    def intersectsWithRocket(cls, component):
        """
        Tests whether or not a component, if placed at the current mouse position, will intersect with the rocket

        :param rockets.Component component: The component class to test
        """
        # make an instance of the component to test with, at the mouse position     
        transform = cls.mousePosToPymunkTransform(component)
        theComponent = component(None, transform=transform)
        cls.theRocket.addComponent(theComponent)

        # update the bounding box for the component
        theComponent.cache_bb()

        # compare on every single component in the rocket
        for rocketComponent in cls.theRocket.components:
            # except for the one we just made...
            if rocketComponent is not theComponent:
                # update the rocket component's bounding box...
                rocketComponent.cache_bb()
                # ...and see if it collides with our shape
                if theComponent.shapes_collide(rocketComponent).points:
                    #if it does, remove the component and return True!
                    cls.theRocket.removeComponent(theComponent)
                    return True

        # if it doesn't for any of the rocket components, remove it and return False
        cls.theRocket.removeComponent(theComponent)
        return False

    @classmethod
    def componentButtonClicked(cls, component) :
        """
        A helper method that changes the selected component. This is used in the buttons in the component list
        
        :param rockets.Component component: The component class to set as active
        """
        cls.activeComponent = component

    @classmethod
    def setCurrentTab(cls, state):
        """
        A helper method that changes the selected tab. This is used in the tab buttons to change the component list.
        """
        cls.selectedTab = state

    @classmethod
    def toggleSymmetry(cls):
        """
        A helper method that toggles the symmetry flag.
        """
        cls._symmetry = not cls._symmetry