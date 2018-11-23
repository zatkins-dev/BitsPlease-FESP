import pygame as pg
from rockets import Component
import math
import os

class Tank(Component):
    _vertices = None
    _sprite = None
    _capacity = None

    def __init__(self, body, transform=None, radius=0):
        Component.__init__(self, body, self.vertices, transform, radius)

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
    def capacity(self):
        return self._capacity
    
    def reset(self):
        super().reset()
        self._fuel = self._capacity

class TestTank(Tank):
    _vertices = [(-6, 18), (-6, -18), (6, -18), (6, 18)]
    _capacity = 20000
    _sprite = pg.image.load(os.path.join("assets", "sprites", "fueltank.png"))

    def __init__(self, body, transform=None, radius=0):
        Tank.__init__(self, body, transform, radius)
        self._fuel = self._capacity

    @classmethod
    def getDisplayInfo(cls):
        pass
        return {
            "Capacity": str(cls._capacity)
        }

        