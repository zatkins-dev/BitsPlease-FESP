from rockets import Component
import pygame as pg
import os
from . import _ASSETS_PATH


class CommandModule(Component):
    _density = 34
    _sprite = pg.image.load(os.path.join(_ASSETS_PATH, "sprites", "orbiter.png")).convert_alpha()

    # Should we choose to make different types of command modules, we will
    # abstract this. For now, we'll just have one

    # def __init__(self, body, vertices, transform=None, radius=0):
    #     Component.__init__(self, body, vertices, transform, radius)

    def __init__(self, body, transform=None, radius=0):
        Component.__init__(self, body, self.vertices, transform, radius)
        self.density = self._density
    
    @property
    def vertices(self):
        return [(12, 4), (-12, 4), (0, 42)]

    @property
    def sprite(self):
        return self._sprite

    def reset(self):
        super().reset()

    @classmethod
    def getDisplayInfo(cls):
        return {
            "Rocket's Base": "The Heart of the Rocket"
        }

