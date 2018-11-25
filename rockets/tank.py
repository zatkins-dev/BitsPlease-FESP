import pygame as pg
from rockets import Component
import math
import os
from . import _ASSETS_PATH

class Tank(Component):
    """
    Tank Component for rocket. Holds fuel for all liquid thrusters to pull from as a source
    Must be attached to a body.
    """
    

    def __init__(self, body, transform=None, radius=0):
        """
        Initializes a Tank

        :param body: Body to attatch the Tank to.
        :type body: :py:class:`pymunk.Body`
        :param transform: Transformation to apply to the shape
        :type transform: :py:class:`pymunk.Transform`
        :param float radius: Radius of the shape, used for smoothing.
        """
        Component.__init__(self, body, self.vertices, self.getInfo()["density"], transform, radius)

    @property
    def fuel(self):
        """
        The current ammount of fuel remaining in the Tank
        """
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
        The sprite of this specific type of Tank. This returns the value defined in the getInfo method.
        """
        return self.getInfo()["sprite"]

    @property
    def vertices(self):
        """
        The vertices of this specific type of Tank. This returns the value defined in the getInfo method.
        """
        return self.getInfo()["vertices"]
    
    @property
    def capacity(self):
        """
        The maximum amount of fuel a tank can hold
        The tank will be initialized with this amount of fuel
        """
        return self._capacity
    
    def reset(self):
        """
        Resets the Tank, resets fuel amount to the capacity
        """
        super().reset()
        self._fuel = self._capacity

class TestTank(Tank):
    """
    The TestTank components will all share these properties:

    +----------------+----------------------------------------------------------------------------------------------------------------------+
    | Dictionary Key |              Dictionary Value Type                                                                                   |
    +================+======================================================================================================================+
    |    vertices    | [(-6, 18), (-6, -18), (6, -18), (6, 18)]                                                                             |        
    +----------------+----------------------------------------------------------------------------------------------------------------------+
    |     sprite     | `TestTank.png <https://github.com/zatkins-school/BitsPlease-FESP/blob/project-4/assets/sprites/TestTank.png>`_       |
    +----------------+----------------------------------------------------------------------------------------------------------------------+
    |     capacity   | 20,000                                                                                                               |
    +----------------+----------------------------------------------------------------------------------------------------------------------+
    |     density    | 73.8                                                                                                                 |
    +----------------+----------------------------------------------------------------------------------------------------------------------+
    """


    _vertices = [(-6, 18), (-6, -18), (6, -18), (6, 18)]
    _capacity = 20000
    _sprite = pg.image.load(os.path.join(_ASSETS_PATH, "sprites", "fueltank.png"))
    _density = 73.8

    def __init__(self, body, transform=None, radius=0):
        Tank.__init__(self, body, transform, radius)
        self._fuel = self._capacity

    @classmethod
    def getInfo(cls):
        """
        Returns unformatted 
        """
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
   
    


        