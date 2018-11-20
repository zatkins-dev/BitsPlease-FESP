from pymunk import Body as Body
import pygame as pg
from rockets import Thruster, RCSThruster
from rockets import SAS


class Rocket(Body):
    """Extends pymunk.Body with helper functions for thruster & steering.

    Args:
        components (List(Component)): List of Components to attach to rocket.

    Attributes:
        thrusters (List(Thruster)): List of Thruster components.
        SASmodules (List(SAS)): List of SAS components.
        angular_velocity_limit (Float): Maximum angular velocity.
        components (List(Component)): List of Components attached to rocket.

    """

    def __init__(self, components=[]):
        Body.__init__(self)
        for c in components:
            c.body = self
        self.components = components
        self.angular_velocity_limit = 400000
        self.destroyed=False
        self.throttle = 0

    @property
    def throttle(self):
        return self._throttle

    @throttle.setter
    def throttle(self, newThrottle):
        # never leave the 0 or 1 range
        if 0 <= newThrottle <= 1:
            self._throttle = newThrottle
        elif newThrottle > 1:
            self._throttle = 1
        elif newThrottle < 0:
            self._throttle = 0

    @property
    def thrusters(self):
        return list(filter(lambda c: isinstance(c, Thruster) and not isinstance(c, RCSThruster), self.components))

    @property
    def SASmodules(self):
        return list(filter(lambda c: isinstance(c, SAS), self.components))

    @property
    def RCSThrusters(self):
        return list(filter(lambda c: isinstance(c, RCSThruster), self.components))

    def tick(self):
        # let SAS modules fire rcs thrusters if needed
        for module in self.SASmodules:
            module.holdAngle()

        # apply all of the thrusters, with the current throttle
        if self.throttle is not 0:
            for thruster in self.thrusters:
                if not thruster.destroyed:
                    thruster.applyThrust(self.throttle)

        

    def handleEvent(self, eventKey):
        if eventKey == pg.K_f : # Apply main thrust
            for ts in self.thrusters:
                # check to make sure this isn't an RCS thruster
                if not isinstance(ts, RCSThruster) and not ts.destroyed:
                    ts.applyThrust(1)
        elif eventKey == pg.K_a : # Counter-Clockwise Rotation
            for sas in self.SASmodules:
                if not sas.destroyed:
                    sas.rotateCounterClockwise()
        elif eventKey == pg.K_d : # Clockwise Rotation
            for sas in self.SASmodules:
                if not sas.destroyed:
                    sas.rotateClockwise()
        elif eventKey == pg.K_v : # Toggle Rotation Lock
            for sas in self.SASmodules:
                if not sas.isAngleLocked:
                    sas.SASangle = self.angle
                sas.toggleAngleLock()
        

    def addComponent(self, c):
        """Add a new component to the rocket

        Args:
            c (Component): Component to attach to rocket

        """
        c.body = self
        self.components.append(c)

    def removeComponent(self, c):
        for x in self.components:
            if x.get_vertices() == c.get_vertices() :
                self.components.remove(x)


    def debugComponentPrint(self):
        for x in self.components :
            print(x.get_vertices())
