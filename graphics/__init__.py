import pygame
if not pygame.display.get_init():
    pygame.init()
    pygame.display.set_mode((854, 480), pygame.RESIZABLE)

from .graphics import Graphics
from .hud import HUD
from .menu import Menu
from .drawer import Drawer
from .trajectory import Trajectory
from .explosion import Explosion
