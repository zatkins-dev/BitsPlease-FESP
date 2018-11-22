from rockets import Component
import pygame as pg
import os


class CommandModule(Component):
    _vertices = [(12, 4), (-12, 4), (0, 42)]
    _density = 34
    _sprite = pg.image.load(os.path.join("assets", "sprites", "orbiter.png"))

    # Should we choose to make different types of command modules, we will
    # abstract this. For now, we'll just have one

    # def __init__(self, body, vertices, transform=None, radius=0):
    #     Component.__init__(self, body, vertices, transform, radius)

    def __init__(self, body, transform=None, radius=0):
        Component.__init__(self, body, self._vertices, transform, radius)
        self.density = self._density
    
    def reset(self):
        super().reset()

    @classmethod
    def getDisplayInfo(cls):
        return {
            "Rocket's Base": "The Heart of the Rocket"
        }

