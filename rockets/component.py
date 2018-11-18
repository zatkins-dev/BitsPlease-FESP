import pygame as pg
import pymunk as pm


class Component(pm.Poly):
    """Extention of pymunk Poly class with properties for sprites/textures.

    Args:
        body (Body): Body to attach component to
        vertices (List(Vec2d)): Vertices of Poly shape
        transform (Transform): Transformation to apply to shape
        radius (Float): Edge radius of shape for smoothing

    Attributes:
        _vertices (list of float, float): list of tuples holding x,y coordinates
        _sprite (pygame.Surface): pygame Surface holding image of component

    """

    _vertices = None
    _sprite = None

    def __init__(self, body, vertices, transform=None, radius=0):
        super().__init__(body, vertices, transform, radius)

    @property
    def vertices(self):
        return self._vertices

    @property
    def sprite(self):
        """Image Sprite for the component

        Returns:
            Surface: Component Sprite
        """
        return self._sprite

    @sprite.setter
    def sprite(self, sprite):
        """Setter for {sprite} property

        Args:
            sprite (surface): New Surface to use as component sprite
        """
        self._sprite = sprite
