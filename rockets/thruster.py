from pymunk.vec2d import Vec2d
from rockets import Component
from pymunk import Body as Body
import pygame as pg
import os


class Thruster(Component):
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

    _vertices = None
    _thrustForce = None
    _thrustVector = None
    _sprite = None
    _maxFuel = None
    _density = None

    def __init__(self, body, vertices=None, thrustForce=None, thrustVector=None, maxFuel=None, density=None, transform=None, radius=0):
        if vertices is not None:
            self._vertices = vertices
        if thrustForce is not None:
            self._thrustForce = thrustForce
        if thrustVector is not None:
            self._thrustVector = thrustVector
        if maxFuel is not None:
            self._maxFuel = maxFuel
        if density is not None:
            self._density = density

        Component.__init__(self, body, self.vertices, transform, radius)

        self.density = self._density
        self.fuel = self.maxFuel

    @property
    def thrustForce(self):
        """Magnitude of thrust

        Returns:
            float: thrust magnitude.

        """
        return self._thrustForce

    @property
    def thrustVector(self):
        """Direction of thrust

        Returns:
            pymunk.Vec2d: direction of thrust adjusted for rocket rotation.

        """
        return self._thrustVector

    @property
    def maxFuel(self):
        return self._maxFuel

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
            self.body.apply_impulse_at_local_point(self.thrust(), (self.center_of_gravity.x, self.center_of_gravity.y))
            self.fuel = self.fuel -1


class RCSThruster(Thruster):
    """An RCS Thruster is intended to be a smaller thruster, that pulls
       fuel from the rocket's SAS fuel instead of its own supply.

    """

    _maxFuel = 0

    def __init__(self, body, vertices=None, thrustForce=None, thrustVector=None, density=None, transform=None, radius=0):
        Thruster.__init__(self, body, vertices, thrustForce, thrustVector, None, density, transform, radius)
    
    def applyThrust(self):
        sasModule = None
        for module in self.body.SASmodules:
            if module.fuel > 0:
                sasModule = module
                break
        if sasModule is not None:
            self.body.apply_impulse_at_local_point(self.thrust(), (self.center_of_gravity.x, self.center_of_gravity.y))
            sasModule.fuel -= 1

class LeftRCS(RCSThruster):
    _vertices = [(0, 37), (5, 37), (5, 42), (0, 42)]
    _thrustForce = 5000
    _thrustVector = Vec2d((-1, 0))
    _sprite = pg.image.load(os.path.join("assets", "sprites", "RCSLeft.png"))
    _density = 45

    def __init(self, body, transform=None, radius=0):
        print(self._vertices)
        Thruster.__init__(self, body, transform=transform, radius=radius)

class RightRCS(RCSThruster):
    _vertices = [(0, 37), (-5, 37), (-5, 42), (0, 42)]
    _thrustForce = 5000
    _thrustVector = Vec2d((1, 0))
    _sprite = pg.image.load(os.path.join("assets", "sprites", "RCSRight.png"))
    _density = 45

    def __init(self, body, transform=None, radius=0):
        print(self._vertices)
        Thruster.__init__(self, body, transform=transform, radius=radius)

                
class DeltaVee(Thruster):
    _vertices = [(4.2, 0), (-4.2, 0), (4.2, 46.9), (-4.2, 46.9)]
    _thrustForce = 50000
    _thrustVector = Vec2d((0,1))
    _sprite = Component.scaleSpriteToVerts(pg.image.load(os.path.join("assets", "sprites", "UpGoer2000.png")), _vertices)
    _maxFuel = 40000
    _density = 73.8
   
    
    def __init__(self, body, transform=None, radius=0):
       Thruster.__init__(self, body, self.vertices, transform=transform, radius=radius)



#class SolidThruster(Thruster):


#class LiquidThruster(Thruster):

