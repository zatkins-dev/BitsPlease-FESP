import pygame
from Graphics import Graphics

class menu(object):

    splashScreenPressed = False

    @classmethod
    def drawSplashScreen(cls):
        surface = pygame.display.get_surface()
        surfaceSize = surface.get_size()
        surfaceCenter = (surfaceSize[0] / 2, surfaceSize[1] / 2)

        #fill surface with black
        surface.fill((0,0,0))

        #draw a button
        Graphics.drawButton(surface, (0,0), surfaceSize, ((0,0,0,0), (0,0,0,0)), 0, 0, cls._splashCallback)

        #In the future, may want to draw an image onto the surface as a background
        #for now, just draw text
        Graphics.drawText(surfaceCenter, "Flat Earth Space Program", 40, (255,255,255))

    @classmethod
    def drawMenu(cls):
        surface = pygame.display.get_surface()
        surfaceSize = surface.get_size()
        surfaceCenter = (surfaceSize[0] / 2, surfaceSize[1] / 2)

        titleCenter = (surfaceCenter[0], surfaceCenter[1] - 100)

        #fill screen with black
        surface.fill((0,0,0))

        Graphics.drawText(titleCenter, "Flat Earth Space Program", 40, (255,255,255))

    @classmethod
    def _splashCallback(cls):
        cls.splashScreenPressed = True