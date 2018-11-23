from pymunk.vec2d import Vec2d
from rockets import Component
from pymunk import Body as Body
import pygame as pg
import os
from abc import ABC, abstractmethod
from . import _ASSETS_PATH


class Thruster(Component):
    """Thruster Interface for creation of thrusters. Individual named
    thrusters inherit from and implement this class. Most of the implementation
    is already done within this interface, with key parts left out for the 
    subclasses to make their own.
    """

    def __init__(self, body, transform=None, radius=0):
        """Constructor for a Thruster. The important things done in this constructor include
        creating the Component base using the vertices defined in the getInfo method, and 
        setting the density and initial fuel of the thruster also using values from the 
        getInfo method.

        :param pymunk.Body body: The body to attatch this thruster to.
        :param pymunk.Transform transform: The transform to apply to the Thruster on creation.
        :param float radius: The radius to give to the Thruster's corners.
        """
        Component.__init__(self, body, self.getInfo()["vertices"], transform, radius)

        self.density = self.getInfo()["density"]
        self.fuel = self.getInfo()["maxFuel"]

    #: The vertices of this specific type of thruster. This returns the value defined in 
    #: the getInfo method.
    @property
    def vertices(self):
        return self.getInfo()["vertices"]

    #: The magnitude of the thrust of this specific type of thruster. This returns the value
    #: defined in the getInfo method.
    @property
    def thrustForce(self):
        return self.getInfo()["thrustForce"]

    #: The direction that the thruster will apply thrust. This returns the value defined
    #: in the getInfo method.
    @property
    def thrustVector(self):
        return self.getInfo()["thrustVector"]

    #: The maximum ammount of fuel that the thruster starts with. This returns the value
    #: defined in the getInfo method.
    @property
    def maxFuel(self):
        return self.getInfo()["maxFuel"]

    #: The current ammout of fuel that the thruster has. Cannot be set below zero.
    @property
    def fuel(self):
        return self._fuel

    @fuel.setter
    def fuel(self, newFuel):
        if newFuel >= 0:
            self._fuel = newFuel
        else:
            self._fuel = 0

    def thrust(self):
        """
        Returns the scaled thrust vector of the Thruster.
        """
        return self.thrustForce * self.thrustVector

    def applyThrust(self, throttle, timescale):
        """
        Applies thrust to the rocket, scaling the thrust to a throttle value between 0 and 1. The 
        thrust provided and fuel consumed are then scaled by the provide timescale.

        :param float throttle: The ammount to throttle the thrust by, between 0 and 1
        :param float timescale: The ammount to scale the thrust provided and fuel consumed.
        """
        if self.fuel > 0 and 0 < throttle <= 1:
            self.body.apply_impulse_at_local_point(throttle * self.thrust() * timescale, (self.center_of_gravity.x, self.center_of_gravity.y))
            self.fuel -= 1 * throttle * timescale

    def reset(self):
        """
        Resets properties of the underlying component and the fuel of the thruster to restart the simulation
        """
        super().reset()
        self._fuel = self.maxFuel

    @classmethod
    @abstractmethod
    def getInfo(cls):
        """This method is what will define the properties of a specific Thruster subclass.
           It should return a dictionary with the following values:

           +----------------+-------------------------------------------------+
           | Dictionary Key |              Dictionary Value Type              |
           +================+=================================================+
           |    vertices    |   (*List of* :py:class:`pymunk.vec2d.Vec2d`)    |
           +----------------+-------------------------------------------------+
           |   thrustForce  |                    (*float*)                    |
           +----------------+-------------------------------------------------+
           |  thrustVector  |        (:py:class:`pymunk.vec2d.Vec2d`)         |
           +----------------+-------------------------------------------------+
           |                | (:py:class:`pygame.surface.Surface`) It is      |
           |     sprite     | advised this be stored as a class variable, and |
           |                | returned by this method to improve performance. |
           +----------------+-------------------------------------------------+
           |     maxFuel    |                    (*float*)                    |
           +----------------+-------------------------------------------------+
           |     density    |                    (*float*)                    |
           +----------------+-------------------------------------------------+
        """
        pass

    @classmethod
    def getDisplayInfo(cls):
        """
        Returns a dictionary containing the "Thrust" and "Thrust Vector" of the rocket
        with units attatched for display to the screen or user.
        """
        inf = cls.getInfo()
        return {
            "Thrust": str(inf["thrustForce"]) + "N",
            "Thrust Vector": str(tuple(inf["thrustVector"])),
        }


class RCSThruster(Thruster):
    """
    An RCS Thruster is intended to be a smaller thruster, that pulls
    fuel from the rocket's SAS fuel instead of its own supply and is
    used for rotation instead of direct motion.
    """

    def __init__(self, body, transform=None, radius=0):
        Component.__init__(self, body, self.getInfo()["vertices"], transform, radius)

        self.density = self.getInfo()["density"]
        self.fuel = 0
    
    def applyThrust(self):
        sasModule = None
        for module in self.body.SASmodules:
            if module.fuel > 0:
                sasModule = module
                break
        if sasModule is not None:
            self.body.apply_impulse_at_local_point(self.thrust(), (self.center_of_gravity.x, self.center_of_gravity.y))
            sasModule.fuel -= 1

    @classmethod
    @abstractmethod
    def getInfo(cls):
        """This method is what will define the properties of a specific RCSThruster subclass.
           It is identical to the Thruster getInfo, but does not need a "maxFuel" member.
           It should return a dictionary with the following values:
                vertices       : (list of tuples)
                thrustForce    : (float)
                thrustVector   : (tuple or pymunk.Vec2d)
                sprite         : (pygame.Surface, advised to store this as a class variable
                                   and return it via this dictionary for performance)
                density        : (float)
        """
        pass

class LeftRCS(RCSThruster):

    _sprite = pg.image.load(os.path.join(_ASSETS_PATH, "sprites", "RCSLeft.png")).convert_alpha()

    def __init(self, body, transform=None, radius=0):
        Thruster.__init__(self, body, transform, radius)

    @classmethod
    def getInfo(cls):
        return {
            "vertices":     [(0, 37), (5, 37), (5, 42), (0, 42)],
            "thrustForce":  5000,
            "thrustVector": Vec2d((-1, 0)),
            "sprite":       cls._sprite,
            "maxFuel":      0,
            "density":      45
        }

class RightRCS(RCSThruster):

    _sprite = pg.image.load(os.path.join(_ASSETS_PATH, "sprites", "RCSRight.png")).convert_alpha()

    def __init(self, body, transform=None, radius=0):
        Thruster.__init__(self, body, transform, radius)

    @classmethod
    def getInfo(cls):
        return {
            "vertices":     [(0, 37), (-5, 37), (-5, 42), (0, 42)],
            "thrustForce":  5000,
            "thrustVector": Vec2d((1, 0)),
            "sprite":       cls._sprite,
            "maxFuel":      0,
            "density":      45
        }

class UpGoer2000(Thruster):
    
    _sprite = pg.image.load(os.path.join(_ASSETS_PATH, "sprites", "UpGoer2000.png")).convert()
   
    def __init__(self, body, transform=None, radius=0):
       Thruster.__init__(self, body, transform,radius)

    @classmethod
    def getInfo(cls):
        return {
            "vertices":     [(4.2, 0), (-4.2, 0), (4.2, 46.9), (-4.2, 46.9)],
            "thrustForce":  50000,
            "thrustVector": Vec2d((0,1)),
            "sprite":       cls._sprite,
            "maxFuel":      10000,
            "density":      73.8
        }
                
class DeltaVee(Thruster):
    
    _sprite = pg.image.load(os.path.join(_ASSETS_PATH, "sprites", "DeltaVee.png")).convert()
    
    def __init__(self, body, transform=None, radius=0):
       Thruster.__init__(self, body, transform, radius)

    @classmethod
    def getInfo(cls):
        return {
            "vertices":     [(12, 0), (-12, 0), (12, 70), (-12, 70)],
            "thrustForce":  500000,
            "thrustVector": Vec2d((0,1)),
            "sprite":       cls._sprite,
            "maxFuel":      40000,
            "density":      73.8
        }



#class SolidThruster(Thruster):


#class LiquidThruster(Thruster):

