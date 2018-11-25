import pygame
import os
_ASSETS_PATH = ""
if os.path.exists(os.path.abspath("assets")):
    _ASSETS_PATH = os.path.abspath("assets")
elif os.path.exists(os.path.abspath("../assets")):
    _ASSETS_PATH = os.path.abspath("../assets")
from .video import Video
Video.init()
from .graphics import Graphics
from .hud import HUD
from .menu import Menu
from .drawer import Drawer
from .trajectory import Trajectory
from .explosion import Explosion
