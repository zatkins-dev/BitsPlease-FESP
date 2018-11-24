import pygame as pg
import pymunk as pm
from physics.collision import CT_COMPONENT
from abc import ABC, abstractmethod

class Component(ABC, pm.Poly):
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

    def __init__(self, body, vertices, transform=None, radius=0):
        super().__init__(body, vertices, transform, radius)
        self.collision_type = CT_COMPONENT
        self.destroyed = False
        
    @property
    @abstractmethod
    def vertices(self):
        pass

    @property
    @abstractmethod
    def sprite(self):
        pass

    @classmethod
    @abstractmethod
    def getDisplayInfo(cls):
        """This will should return a dictionary that contains relevant
           Information to display in the rocket builder
        """
        pass

    @abstractmethod
    def reset(self):
        self.destroyed = False