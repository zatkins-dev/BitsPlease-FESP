from abc import ABC, abstractmethod
from pymunk.vec2d import Vec2d
from rockets import Component
from pymunk import Body as Body
import pygame as pg
import os


class Thruster(ABC, Component):
    """Thruster component for rocket. Provides encapsulation for
       thrust direction and magnitude. Must be attached to a body.

    Args:
        body (pymunk.Body): body thruster is attached to.
        vertices (list(pymunk.Vec2d)): vertices of polygon shape.
        thrustVector (pymunk.Vec2d): direction of thrust (relative to Rocket).
        netThrust (float): magnitude of thrust.
        transform (float): transformation to be applied to shape.
        radius (float): edge radius of shape (smoothing).

    Attributes:
        _thrustVector (pymunk.Vec2d): direction of thrust (relative to Rocket).
        _thrustForce (float): magnitude of thrust.
        _fuel (int): current thruster fuel.

    """

    @abstractmethod
    def __init__(self, body, transform=None, radius=0):
        pass

    @property
    @abstractmethod
    def vertices(self):
        pass

    @property
    @abstractmethod
    def thrustForce(self):
        """Magnitude of thrust

        Returns:
            float: thrust magnitude.

        """
        pass

    @property
    @abstractmethod
    def thrustVector(self):
        """Direction of thrust

        Returns:
            pymunk.Vec2d: direction of thrust adjusted for rocket rotation.

        """
        pass

    @property
    @abstractmethod
    def sprite(self):
        pass

    @property
    @abstractmethod
    def maxFuel(self):
        pass

    @property
    def fuel(self):
        return self._fuel

    @fuel.setter
    def fuel(self, newFuel):
        if newFuel >= 0:
            self._fuel = newFuel

    def thrust(self):
        """Gets the scaled thrust vector for application of forces

        Returns:
            pymunk.Vec2d: Scaled thrust vector.

        """
        return self.thrustForce * self.thrustVector

    def applyThrust(self):
        if self.fuel > 0:
            self.body.apply_impulse_at_local_point(self.thrust(), (0, 0))
            self.fuel = self.fuel -1


"""class RCS(Thruster):
        def __init__(self, body, vertices, netThrust, transform, radius, _fuel):
            Thruster.__init__(self, body, vertices, (1,0), newThrust, None, 0)
        #tell the thrust vector to go horiz
        def applyThrust(self, direction):
            #TODO: make thrust able to go both directions(left/right)
            if body.SASfuel > 0:
                self.body.apply_impulse_at_local_pont(Thruster.thrust(), (0,0))"""
                
class DeltaVee(Thruster):

    _vertices = [(4.2, 0), (-4.2, 0), (4.2, 46.9), (-4.2, 46.9)]
    _thrustForce = 50000
    _thrustVector = Vec2d((0,1))
    _sprite = pg.image.load(os.path.join("assets", "sprites", "UpGoer2000.png"))
    _maxFuel = 40000
    
    def __init__(self, body, transform=None, radius=0):
        Component.__init__(self, body, self.vertices, transform, radius)
        self._fuel = self.maxFuel

    @property
    def vertices(self):
        return self._vertices

    @property
    def thrustForce(self):
        return self._thrustForce

    @property
    def thrustVector(self):
        return self._thrustVector

    @property
    def sprite(self):
        return self._sprite

    @property
    def maxFuel(self):
        return self._maxFuel




#class SolidThruster(Thruster):


#class LiquidThruster(Thruster):

