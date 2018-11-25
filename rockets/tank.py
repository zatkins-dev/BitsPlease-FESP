import pygame as pg
from rockets import Component
import math
import os

class Tank(Component):
    

    def __init__(self, body, transform=None, radius=0):
        Component.__init__(self, body, self.vertices, self.getInfo()["density"], transform, radius)

    @property
    def fuel(self):
        return self._fuel

    @fuel.setter
    def fuel(self, newFuel):
        if newFuel > 0:
            self._fuel = newFuel
            return True 
        else:
            self._fuel = 0
            return False #empty flag

    @property
    def sprite(self):
        """
        The sprite of this specific type of SASModule. This returns the value defined in
        the getInfo method.
        """
        return self.getInfo()["sprite"]

    @property
    def vertices(self):
        """
        The vertices of this specific type of SASModule. This returns the value defined in
        the getInfo method.
        """
        return self.getInfo()["vertices"]
    
    @property
    def capacity(self):
        return self._capacity
    
    def reset(self):
        super().reset()
        self._fuel = self._capacity

class TestTank(Tank):
    _vertices = [(-6, 18), (-6, -18), (6, -18), (6, 18)]
    _capacity = 20000
    _sprite = pg.image.load(os.path.join("assets", "sprites", "fueltank.png"))
    _density = 73.8

    def __init__(self, body, transform=None, radius=0):
        Tank.__init__(self, body, transform, radius)
        self._fuel = self._capacity

    @classmethod
    def getInfo(cls):
        return {
            "vertices":     [(-6, 18), (-6, -18), (6, -18), (6, 18)],
            "sprite":       cls._sprite,
            "density":      73.8,
            "capacity":     cls._capacity
        }
    
    @classmethod
    def getDisplayInfo(self):
        inf = self.getInfo()
        return{ "Capacity": str(inf["capacity"])}
   
    


        