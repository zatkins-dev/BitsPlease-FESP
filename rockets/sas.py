import pygame as pg
from rockets import Component
import math
import os
from abc import ABC, abstractmethod
from . import _ASSETS_PATH

class SAS(Component):
    """
    SAS component for rocket. Provides encapsulation for
    SAS autonomous angle and magnitude of SAS force.
    Must be attached to a body.
    """

    def __init__(self, body, transform=None, radius=0):
        """
        Initializes an SAS Module: the underlying component, and the angle & fuel value.

        :param body: Body to attatch the SASModule to.
        :type body: :py:class:`pymunk.Body`
        :param transform: Transformation to apply to the shape
        :type transform: :py:class:`pymunk.Transform`
        :param float radius: Radius of the shape, used for smoothing.
        """
        Component.__init__(self, body, self.vertices, self.getInfo()["density"], transform, radius)
        self._SASangle = 0
        self.fuel = self.maxFuel

    @property
    def fuel(self):
        """
        The current ammount of fuel that the SAS module has for maneuvering.
        """
        return self._fuel

    @fuel.setter
    def fuel(self, newFuel):
        if newFuel > 0:
            self._fuel = newFuel
        else:
            self._fuel = 0

    def rotateCounterClockwise(self, timescale):
        """
        Uses the RCS Thrusters on the host rocket to turn the rocket counter-clockwise.
        """

        for ts in self.body.RCSThrusters:
            # check the direction of each thruster, and apply if it will rotate counter clockwise
            if ts.thrustVector.x < 0 and ts.center_of_gravity.y > self.body.center_of_gravity.y:
                # left-directed vector and on the top half of the rocket
                ts.applyThrust(timescale)
            elif ts.thrustVector.x > 0 and ts.center_of_gravity.y < self.body.center_of_gravity.y:
                # right-directed vector and on the bottom half of the rocket
                ts.applyThrust(timescale)

    def rotateClockwise(self, timescale):
        """
        Uses the RCS Thrusters on the host rocket to turn the rocket clockwise.
        """

        for ts in self.body.RCSThrusters:
            # check the direction of each thruster, and apply if it will rotate clockwise
            if ts.thrustVector.x > 0 and ts.center_of_gravity.y > self.body.center_of_gravity.y:
                # right-directed vector and on the top half of the rocket
                ts.applyThrust(timescale)
            elif ts.thrustVector.x < 0 and ts.center_of_gravity.y < self.body.center_of_gravity.y:
                # left-directed vector and on the bottom half of the rocket
                ts.applyThrust(timescale)

    def holdAngle(self, timescale):
        """
        Will work to hold the rocket at the set SASAngle. This is affected by the SASPower and the Tolerance
        parameters of a specific SAS Module.
        """

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
                self.rotateCounterClockwise(timescale)
            elif targetAngVel < self.body.angular_velocity:
                self.rotateClockwise(timescale)

    def reset(self):
        """
        Resets the SAS Module, including the set angle and fuel ammount.
        """
        super().reset()
        self._SASangle = 0
        self._fuel = self.maxFuel

    @property
    def SASangle(self):
        """
        Lock angle in radians for the SAS
        """
        return self._SASangle

    @SASangle.setter
    def SASangle(self, newAngle):
        self._SASangle = newAngle

    @property
    def vertices(self):
        """
        The vertices of this specific type of SASModule. This returns the value defined in
        the getInfo method.
        """
        return self.getInfo()["vertices"]

    @property
    def SASPower(self):
        """
        The SASPower of this specific type of SASModule. This returns the value defined in
        the getInfo method.
        """
        return self.getInfo()["SASPower"]

    @property
    def tolerance(self):
        """
        The angle tolerance of this specific type of SASModule. This returns the value defined in
        the getInfo method.
        """
        return self.getInfo()["tolerance"]

    @property
    def sprite(self):
        """
        The sprite of this specific type of SASModule. This returns the value defined in
        the getInfo method.
        """
        return self.getInfo()["sprite"]
    
    @property
    def maxFuel(self):
        """
        The maximum fuel ammount of this specific type of SASModule. This returns the value defined in
        the getInfo method.
        """
        return self.getInfo()["maxFuel"]

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

    @classmethod
    def getInfo(cls):
        """
        Returns the dictionary with info specified by SAS.getInfo()
        """
        return {
            "vertices":     [(-12,4), (-12,-6), (12,-6), (12,4)],
            "SASPower":  2,
            "tolerance": .01,
            "sprite":       cls._sprite,
            "maxFuel":      20000,
            "density":      100
        }
