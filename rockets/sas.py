import pygame as pg
from rockets import Component
import math
import os
from abc import ABC, abstractmethod
from . import _ASSETS_PATH



class SAS(Component):
    """SAS component for rocket. Provides encapsulation for
       SAS autonomous angle and magnitude of SAS force.
       Must be attached to a body.

    Args:
        body (Body): Rocket body to attach to
        vertices (List(Vec2d)): Vertices of Poly shape
        SASpower (Float): Rotation rate of the rocket from the SAS module
        angle (Float): Lock angle for the SAS
        transform (Transform): Transformation to apply to shape
        radius (Float): Edge radius of shape for smoothing

    Attributes:
        _SASangle (Float): Lock angle for the SAS
        _SASpower (Float): Rotation rate of the rocket from the SAS module
        leftKey (Int): Key to activate left SAS.
        rightKey (Int): Key to activate right SAS.
        fuel (Int): Number game ticks of remaining fuel.

    """

    def __init__(self, body, transform=None, radius=0):
        Component.__init__(self, body, self.vertices, transform, radius)
        self._SASangle = 0

    @property
    def fuel(self):
        return self._fuel

    @fuel.setter
    def fuel(self, newFuel):
        if newFuel > 0:
            self._fuel = newFuel
        else:
            self._fuel = 0

    def rotateCounterClockwise(self):
        for ts in self.body.RCSThrusters:
            # check the direction of each thruster, and apply if it will rotate counter clockwise
            if ts.thrustVector.x < 0 and ts.center_of_gravity.y > self.body.center_of_gravity.y:
                # left-directed vector and on the top half of the rocket
                ts.applyThrust()
            elif ts.thrustVector.x > 0 and ts.center_of_gravity.y < self.body.center_of_gravity.y:
                # right-directed vector and on the bottom half of the rocket
                ts.applyThrust()

    def rotateClockwise(self):
        for ts in self.body.RCSThrusters:
            # check the direction of each thruster, and apply if it will rotate clockwise
            if ts.thrustVector.x > 0 and ts.center_of_gravity.y > self.body.center_of_gravity.y:
                # right-directed vector and on the top half of the rocket
                ts.applyThrust()
            elif ts.thrustVector.x < 0 and ts.center_of_gravity.y < self.body.center_of_gravity.y:
                # left-directed vector and on the bottom half of the rocket
                ts.applyThrust()

    def holdAngle(self):
        # move to desired angle
        # find the difference between the current angle and the desired angle
        deltaAngle = self.SASangle - self.body.angle
        if deltaAngle > math.pi:
            deltaAngle = self.SASangle - self.body.angle - 2 * math.pi

        # now we know how far off we are from the desired angle
        # we can check if we're outside the tolerances to move
        if deltaAngle < -1 * self.tolerance or deltaAngle > self.tolerance:
            # we're outside the expected tolerance, so we need to
            # translate the angle into a desired angular velocity
            targetAngVel = .5 * math.atan(self.SASPower * deltaAngle)

            if targetAngVel > self.body.angular_velocity:
                self.rotateCounterClockwise()
            elif targetAngVel < self.body.angular_velocity:
                self.rotateClockwise()

    def reset(self):
        super().reset()
        self._SASangle = 0
        self._fuel = self.maxFuel

    @property
    def SASangle(self):
        """Lock angle in radians for the SAS

        Returns:
            Float: Value of _SASangle

        """
        return self._SASangle

    @SASangle.setter
    def SASangle(self, newAngle):
        """Setter for _SASangle

        Args:
            newAngle (Float): New value for _SASangle

        """
        self._SASangle = newAngle

    @property
    def vertices(self):
        return self.getInfo()["vertices"]

    @property
    def SASPower(self):
        return self.getInfo()["SASPower"]

    @property
    def tolerance(self):
        return self.getInfo()["tolerance"]

    @property
    def sprite(self):
        return self.getInfo()["sprite"]
    
    @property
    def maxFuel(self):
        return self.getInfo()["maxFuel"]

    @property
    def density(self):
        return self.getInfo()["density"]

    @classmethod
    @abstractmethod
    def getInfo(cls):
        """
        This method is what will define the properties of a specific SAS subclass.
        It should return a dictionary with the following values:

        +----------------+-------------------------------------------------+
        | Dictionary Key |              Dictionary Value Type              |
        +================+=================================================+
        |    vertices    |   (*List of* :py:class:`pymunk.vec2d.Vec2d`)    |
        +----------------+-------------------------------------------------+
        |    SASPower    |                    (*float*)                    |
        +----------------+-------------------------------------------------+
        |    tolerance   |        (:py:class:`pymunk.vec2d.Vec2d`)         |
        +----------------+-------------------------------------------------+
        |                | (:py:class:`pygame.surface.Surface`) It is      |
        |     sprite     | advised this be stored as a class variable, and |
        |                | returned by this method to improve performance. |
        +----------------+-------------------------------------------------+
        |     maxFuel    |             (*float*) Should always be 0        |
        +----------------+-------------------------------------------------+
        |     density    |                    (*float*)                    |
        +----------------+-------------------------------------------------+
        """
        pass

    @classmethod
    def getDisplayInfo(cls):
        inf = cls.getInfo()
        return {
            "SAS Power": str(inf["SASPower"]),
            "Tolerance": str(round(math.degrees(inf["tolerance"]), 2)) + "°",
            "RCS Fuel" : str(inf["maxFuel"]) + "L"
        }


class AdvancedSAS(SAS):

    """
    The AdvancedSAS components will all share these properties:

    +----------------+----------------------------------------------------------------------------------------------------------------------+
    | Dictionary Key |              Dictionary Value Type                                                                                   |
    +================+======================================================================================================================+
    |    vertices    | [(-12,4), (-12,-6), (12,-6), (12,4)]                                                                                 |        
    +----------------+----------------------------------------------------------------------------------------------------------------------+
    |    SASPower    | 2.0                                                                                                                  |
    +----------------+----------------------------------------------------------------------------------------------------------------------+
    |    tolerance   | .01                                                                                                                  |
    +----------------+----------------------------------------------------------------------------------------------------------------------+
    |     sprite     | `AdvancedSAS.png <https://github.com/zatkins-school/BitsPlease-FESP/blob/project-4/assets/sprites/AdvancedSAS.png>`_ |
    +----------------+----------------------------------------------------------------------------------------------------------------------+
    |     maxFuel    | 20,000                                                                                                               |
    +----------------+----------------------------------------------------------------------------------------------------------------------+
    |     density    | 73.8                                                                                                                 |
    +----------------+----------------------------------------------------------------------------------------------------------------------+
    """

    #: Holds the SAS sprite to prevent repeated loading. Sprite is 
    #: `AdvancedSAS.png <https://github.com/zatkins-school/BitsPlease-FESP/blob/project-4/assets/sprites/AdvancedSAS.png>`_
    _sprite = pg.image.load(os.path.join(_ASSETS_PATH, "sprites", "AdvancedSAS.png"))

    def __init__(self, body, transform=None, radius=0):
        SAS.__init__(self, body, transform, radius)
        self._fuel = self.maxFuel

    @classmethod
    def getInfo(cls):
        return {
            "vertices":     [(-12,4), (-12,-6), (12,-6), (12,4)],
            "SASPower":  2,
            "tolerance": .01,
            "sprite":       cls._sprite,
            "maxFuel":      20000,
            "density":      100
        }
