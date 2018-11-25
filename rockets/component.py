import pygame as pg
import pymunk as pm
from physics.collision import CT_COMPONENT
from abc import ABC, abstractmethod

class Component(ABC, pm.Poly):
    """
    Extention of pymunk Poly class with properties for sprites/textures and shape (vertices)
    """

    def __init__(self, body, vertices, density, transform=None, radius=0):
        """
        Passes the given parameters on to the underlying Pymunk shape, and initializes
        some collision management and the destroyed status of the component.

        :param body: Body to attatch the component to.
        :type body: :py:class:`pymunk.Body`
        :param vertices: Verticies of the shape
        :type vertices: list(:py:class:`pymunk.vec2d.Vec2d`)
        :param transform: Transformation to apply to the shape
        :type transform: :py:class:`pymunk.Transform`
        :param float radius: Radius of the shape, used for smoothing.
        """

        super().__init__(body, vertices, transform, radius)
        self.density = density
        self.collision_type = CT_COMPONENT
        self.destroyed = False
        
    @property
    @abstractmethod
    def vertices(self):
        """
        This should return the vertices of the component
        """
        pass

    @property
    @abstractmethod
    def sprite(self):
        """
        This should return a surface that represents the component's sprite/texture
        """
        pass

    @classmethod
    @abstractmethod
    def getDisplayInfo(cls):
        """
        This will should return a dictionary that contains relevant
        "pretty" Information to display in the rocket builder
        """
        pass

    @abstractmethod
    def reset(self):
        """
        Resets the destroyed status of the component.
        """
        self.destroyed = False