import pygame
from graphics import Graphics
from enum import Enum

class Menu(object):
    """
    Menu is a class with methods that can draw different menu items or screens
    to the display.
    """

    #: The different states that the menu can take
    State = Enum('State', 'Splash Menu Building Playing Exit')

    #: Becomes true when the first screen (title screen) has been clicked on.
    #: A higher order class can watch this and proceed to the actual menu.
    splashScreenPressed = False

    #: Becomes true when the "start demo" button has been pressed. A higher order
    #: class can watch this and take appropriate action on change
    demoPressed = False

    #: Becomes true when the Rocket builder button has been pressed. A higher
    #: order class can watch htis and take appropriate action on change. 
    builderPressed = False

    #: Becomes true when a the quit button has been pressed. A higher order class can
    #: watch this and take appropriate action on change
    quitPressed = False

    #: The color to use for the menu buttons
    _menuButtonColor = ((255, 255, 255, 64), (255, 255, 255, 128))

    @classmethod
    def drawBackground(cls, color_rgb, opacity):
        """
        Draws the background using the given color and opacity alpha value.

        :param color_rgb: The color of the background
        :type color_rgb: tuple(int, int, int)
        :param int opacity: The alpha value with which to draw the background
        """
        dispSurface = pygame.display.get_surface()
        surfaceSize = dispSurface.get_size()
        background = pygame.surface.Surface(surfaceSize)
        background.fill(color_rgb)
        background.set_alpha(opacity)
        dispSurface.blit(background, (0,0))

    @classmethod
    def drawSplashScreen(cls, opacity):
        """
        Draws the title screen to pygame's current display surface.

        :param int opacity: The alpha value with which to draw the splash screen background
        """
        surface = pygame.display.get_surface()
        surfaceSize = surface.get_size()
        surfaceCenter = (surfaceSize[0] / 2, surfaceSize[1] / 2)
        titleCenter = (surfaceCenter[0], surfaceCenter[1] - 20)
        subtitleCenter = (surfaceCenter[0], surfaceCenter[1] + 20)

        # fill surface with black
        cls.drawBackground((0, 0, 0), opacity)

        # draw a button
        Graphics.drawButton(surface, (0, 0), surfaceSize,
                            ((0, 0, 0, 0), (0, 0, 0, 0)),
                            0, 0, cls._splashCallback)

        # In the future, may want to draw an image onto the surface
        # as a background
        # for now, just draw text
        titleFont = pygame.font.SysFont("lucidaconsole", 40)
        subtitleFont = pygame.font.SysFont("lucidaconsole", 20)

        Graphics.drawTextCenter(titleCenter, "Flat Earth Space Program",
                                titleFont, (255, 255, 255))
        Graphics.drawTextCenter(subtitleCenter, "Click Anywhere to Continue",
                                subtitleFont, (255, 255, 255))

    @classmethod
    def drawMenu(cls, opacity):
        """
        Draws the menu screen and buttons to pygame's current display surface.
        
        :param int opacity: The alpha value with which to draw the menu background
        """
        surface = pygame.display.get_surface()
        surfaceSize = surface.get_size()
        surfaceCenter = (surfaceSize[0] / 2, surfaceSize[1] / 2)

        titleCenter = (surfaceCenter[0], surfaceCenter[1] - 100)

        # fill screen with black
        cls.drawBackground((0, 0, 0), opacity)

        buttonSize = (400, 50)
        buttonPosition = lambda i: (surfaceCenter[0] - buttonSize[0]/2,
                                    surfaceCenter[1] - buttonSize[1]/2 + 65*i)
        titleFont = pygame.font.SysFont("lucidaconsole", 40)

        Graphics.drawTextCenter(titleCenter, "Flat Earth Space Program",
                                titleFont, (255,255,255))
        Graphics.drawButton(surface, buttonPosition(0), buttonSize,
                            cls._menuButtonColor, "Start Demo", 25,
                            cls._demoCallback)
        Graphics.drawButton(surface, buttonPosition(1), buttonSize,
                            cls._menuButtonColor, "Rocket Builder", 25,
                            cls._builderCallback)
        Graphics.drawButton(surface, buttonPosition(2), buttonSize,
                            cls._menuButtonColor, "Exit to Desktop", 25,
                            cls._quitCallback)

    @classmethod
    def _splashCallback(cls):
        """
        Callback function to be called when the title screen is clicked. This sets the
        splashScreenPressed bool to be true.
        """
        cls.splashScreenPressed = True

    @classmethod
    def _builderCallback(cls):
        """
        Callback function to be called when the Rocket Builder button is clicked. This sets the
        builderPressed bool to be true.
        """
        cls.builderPressed = True

    @classmethod
    def _quitCallback(cls):
        """
        Callback function to be called when the quit button is clicked. This sets the
        quitPressed bool to be true.
        """
        cls.quitPressed = True

    @classmethod
    def _demoCallback(cls):
        """
        Callback function to be called when the "start demo" button is clicked. This sets the
        demoPressed bool to be true.
        """
        cls.demoPressed = True
