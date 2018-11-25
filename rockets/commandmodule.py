from rockets import Component
import pygame as pg
import os
from . import _ASSETS_PATH


class CommandModule(Component):
    """
    The CommandModule doesn't serve much purpose on its own other than being a shape with
    collision and a sprite. It is supposed to represent the center/heart of the rocket, being
    a cockpit for its hypothetical crew.
    """

    #: The density of the command module.
    _density = 34

    #: The sprite of the command module.
    _sprite = pg.image.load(os.path.join(_ASSETS_PATH, "sprites", "orbiter.png")).convert_alpha()

    # Should we choose to make different types of command modules, we will
    # abstract this. For now, we'll just have one

    def __init__(self, body, transform=None, radius=0):
        """
        Create a command module attatched to the given body, and at the given transform.

        :param body: The body to attatch the command module to.
        :type body: :py:class:`pymunk.Body`
        :param transform: The transform to apply to the command module on creation.
        :type transform: :py:class:`pymunk.Transform `
        :param float radius: The radius to give to the command module's corners.
        """
        Component.__init__(self, body, self.vertices, self._density, transform, radius)
    
    @property
    def vertices(self):
        """
        The vertices of the shape of the Command Module.
        """
        return [(12, 4), (-12, 4), (0, 42)]

    @property
    def sprite(self):
        """
        The sprite of the command module.
        """
        return self._sprite

    def reset(self):
        """
        Reset the command module's underlying component
        """
        super().reset()

    @classmethod
    def getDisplayInfo(cls):
        """
        Return "pretty" info for disply in the rocket builder
        """
        return {
            "Rocket's Base": "The Heart of the Rocket"
        }

