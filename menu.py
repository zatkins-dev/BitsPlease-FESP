import pygame
from Graphics import Graphics

class menu(object):

    splashScreenPressed = False

    @classmethod
    def drawSplashScreen(cls):
        surface = pygame.display.get_surface()
        surfaceSize = surface.get_size()
        surfaceCenter = (surfaceSize[0] / 2, surfaceSize[1] / 2)

        #fill surface with white
        Graphics.drawButton(surface, (0,0), surfaceSize, ((0,0,0,0), (0,0,0,0)), 0, 0, cls._splashCallback)

        #In the future, may want to draw an image onto the surface as a background
        #for now, just draw text

    @classmethod
    def _splashCallback(cls):
        cls.splashScreenPressed = True