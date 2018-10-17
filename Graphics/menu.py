import pygame
from Graphics.Graphics import Graphics

class menu(object):

    splashScreenPressed = False

    demoPressed = False
    quitPressed = False

    _menuButtonColor = ((255,255,255,64), (255,255,255,128))

    @classmethod
    def drawSplashScreen(cls):
        surface = pygame.display.get_surface()
        surfaceSize = surface.get_size()
        surfaceCenter = (surfaceSize[0] / 2, surfaceSize[1] / 2)
        titleCenter = (surfaceSize[0] / 2, surfaceSize[1] / 2 - 20)
        subtitleCenter = (surfaceSize[0] / 2, surfaceSize[1] / 2 + 20)

        #fill surface with black
        surface.fill((0,0,0))

        #draw a button
        Graphics.drawButton(surface, (0,0), surfaceSize, ((0,0,0,0), (0,0,0,0)), 0, 0, cls._splashCallback)

        #In the future, may want to draw an image onto the surface as a background
        #for now, just draw text
        Graphics.drawText(titleCenter, "Flat Earth Space Program", 40, (255,255,255))
        Graphics.drawText(subtitleCenter, "Click Anywhere to Continue", 20, (255,255,255))

    @classmethod
    def drawMenu(cls):
        surface = pygame.display.get_surface()
        surfaceSize = surface.get_size()
        surfaceCenter = (surfaceSize[0] / 2, surfaceSize[1] / 2)

        titleCenter = (surfaceCenter[0], surfaceCenter[1] - 100)

        #fill screen with black
        surface.fill((0,0,0))

        buttonSize = (400, 50)
        buttonPosition = lambda i:(surfaceCenter[0] - buttonSize[0] / 2, surfaceCenter[1] - buttonSize[1] / 2 + 65 * i)

        Graphics.drawText(titleCenter, "Flat Earth Space Program", 40, (255,255,255))
        Graphics.drawButton(surface, buttonPosition(0), buttonSize, cls._menuButtonColor, "Start Demo", 25,cls._demoCallback)
        Graphics.drawButton(surface, buttonPosition(1), buttonSize, cls._menuButtonColor, "Exit to Desktop", 25, cls._quitCallback)

    @classmethod
    def _splashCallback(cls):
        cls.splashScreenPressed = True

    @classmethod
    def _quitCallback(cls):
        cls.quitPressed = True

    @classmethod
    def _demoCallback(cls):
        cls.demoPressed = True