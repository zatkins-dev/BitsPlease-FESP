from pymunk.vec2d import Vec2d
from rockets import Component
from pymunk import Body as Body
import pygame as pg
import os
from abc import ABC, abstractmethod


class Thruster(Component):
    """Thruster component for rocket. Provides encapsulation for
       thrust direction and magnitude. Must be attached to a body.

    Args:
        body (pymunk.Body): body thruster is attached to.
        vertices (list(pymunk.Vec2d)): vertices of polygon shape.
        thrustVector (pymunk.Vec2d): direction of thrust (relative to Rocket).
        thrustForce (float): magnitude of thrust.
        transform (float): transformation to be applied to shape.
        radius (float): edge radius of shape (smoothing).

    Attributes:
        _thrustVector (pymunk.Vec2d): direction of thrust (relative to Rocket).
        _thrustForce (float): magnitude of thrust.
        _fuel (int): current thruster fuel.

    """

    _infoDict = {
        "vertices": None,
        "thrustForce": None,
        "thrustVector": None,
        "sprite": None,
        "maxFuel": None,
        "density": None
    }

    def __init__(self, body, vertices=None, thrustForce=None, thrustVector=None, maxFuel=None, density=None, transform=None, radius=0):
        if vertices is not None:
            self.getInfo()["vertices"] = vertices
        if thrustForce is not None:
            self.getInfo()["thrustForce"] = thrustForce
        if thrustVector is not None:
            self.getInfo()["thrustVector"] = thrustVector
        if maxFuel is not None:
            self.getInfo()["maxFuel"] = maxFuel
        if density is not None:
            self.getInfo()["density"] = density

        Component.__init__(self, body, self.getInfo()["vertices"], transform, radius)

        self.density = self.getInfo()["density"]
        self.fuel = self.getInfo()["maxFuel"]

    @property
    def vertices(self):
        return self.getInfo()["vertices"]

    @property
    def thrustForce(self):
        """Magnitude of thrust

        Returns:
            float: thrust magnitude.

        """
        return self.getInfo()["thrustForce"]

    @property
    def thrustVector(self):
        """Direction of thrust

        Returns:
            pymunk.Vec2d: direction of thrust adjusted for rocket rotation.

        """
        return self.getInfo()["thrustVector"]

    @property
    def maxFuel(self):
        return self.getInfo()["maxFuel"]

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
        """Gets the scaled thrust vector for application of forces

        Returns:
            pymunk.Vec2d: Scaled thrust vector.

        """
        return self.thrustForce * self.thrustVector

    def applyThrust(self, throttle):
        if self.fuel > 0 and 0 < throttle <= 1:
            self.body.apply_impulse_at_local_point(throttle * self.thrust(), (self.center_of_gravity.x, self.center_of_gravity.y))
            self.fuel -= 1 * throttle

    @classmethod
    @abstractmethod
    def getInfo(cls):
        """This method is what will define the properties of a specific Thruster subclass.
           It should return a dictionary with the following values: {
                    vertices       : (list of tuples)
                    thrustForce    : (float)
                    thrustVector   : (tuple or pymunk.Vec2d)
                    sprite         : (pygame.Surface, advised to store this as a class variable
                                      and return it via this dictionary for performance)
                    maxFuel        : (float)
                    density        : (float)
                }
        """
        pass

    @classmethod
    def getDisplayInfo(cls):
        inf = cls.getInfo()
        return {
            "Thrust": str(inf["thrustForce"]) + "N",
            "Thrust Vector": str(tuple(inf["thrustVector"])),
        }


class RCSThruster(Thruster):
    """An RCS Thruster is intended to be a smaller thruster, that pulls
       fuel from the rocket's SAS fuel instead of its own supply.

    """

    def __init__(self, body, vertices=None, thrustForce=None, thrustVector=None, density=None, transform=None, radius=0):
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

    _sprite = pg.image.load(os.path.join("assets", "sprites", "RCSLeft.png"))

    def __init(self, body, transform=None, radius=0):
        Thruster.__init__(self, body, transform=transform, radius=radius)

    @classmethod
    def getInfo(cls):
        return {
            "vertices":     [(0, 37), (5, 37), (5, 42), (0, 42)],
            "thrustForce":  5000,
            "thrustVector": Vec2d((-1, 0)),
            "sprite":       cls._sprite,
            "density":      45
        }

class RightRCS(RCSThruster):

    _sprite = pg.image.load(os.path.join("assets", "sprites", "RCSRight.png"))

    def __init(self, body, transform=None, radius=0):
        Thruster.__init__(self, body, transform=transform, radius=radius)

    @classmethod
    def getInfo(cls):
        return {
            "vertices":     [(0, 37), (-5, 37), (-5, 42), (0, 42)],
            "thrustForce":  5000,
            "thrustVector": Vec2d((1, 0)),
            "sprite":       cls._sprite,
            "density":      45
        }

class UpGoer2000(Thruster):
    
    _sprite = pg.image.load(os.path.join("assets", "sprites", "UpGoer2000.png"))
   
    def __init__(self, body, transform=None, radius=0):
       Thruster.__init__(self, body, self.vertices, transform=transform, radius=radius)

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
    
    _sprite = pg.image.load(os.path.join("assets", "sprites", "UpGoer2000.png"))
    
    def __init__(self, body, transform=None, radius=0):
       Thruster.__init__(self, body, self.vertices, transform=transform, radius=radius)

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

