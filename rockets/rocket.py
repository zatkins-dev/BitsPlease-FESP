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
        self.isAngleLocked = False

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
    def Tanks(self):
        return list(filter(lambda c: isinstance(c, Tank), self.components))

    @property
    def isAngleLocked(self):
        return self._isAngleLocked

    @isAngleLocked.setter
    def isAngleLocked(self, newAngleLocked):
        if len(self.SASmodules) is not 0:
            self._isAngleLocked = newAngleLocked
            for sas in self.SASmodules:
                sas.SASangle = self.angle
        else:
            self._isAngleLocked = False

    @property
    def RCSThrusters(self):
        return list(filter(lambda c: isinstance(c, RCSThruster), self.components))

    def tick(self, timescale):
        # grab the keyboard state
        currentKeys = pg.key.get_pressed()

        # Check for throttle commands from user
        if currentKeys[pg.K_LSHIFT]:    # increase throttle
            self.throttle += .01
        if currentKeys[pg.K_LCTRL]:     # decrease throttle
            self.throttle -= .01
        if currentKeys[pg.K_z]:         # full throttle
            self.throttle = 1
        if currentKeys[pg.K_x]:         # cut throttle
            self.throttle = 0

        # let SAS modules fire rcs thrusters if needed,
        # checking from input from users if not holding
        if self.isAngleLocked:
            for module in self.SASmodules:
                module.holdAngle()
        else:
            for module in self.SASmodules:
                if currentKeys[pg.K_a]:
                    module.rotateCounterClockwise()
                if currentKeys[pg.K_d]:
                    module.rotateClockwise()

        # apply all of the thrusters, with the current throttle
        if self.throttle is not 0:
            for thruster in self.thrusters:
                if not thruster.destroyed:
                    thruster.applyThrust(self.throttle, timescale)

        

    def handleEvent(self, event):
        if event.type is pg.KEYDOWN:
            # new key has been pressed, place edge sensitive
            # commands in here, i.e. things that only run once
            # per key press
            if event.key is pg.K_v:  # Toggle SAS Lock
                self.isAngleLocked = not self.isAngleLocked
        

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
    
    def decreaseFuel(self, amnt):
        if self.getTotalFuel() > 0:
            for x in self.Tanks :
                if x.fuel(x.fuel - amnt):
                    return True
        return False
        

    def getTotalFuel(self):
        totalFuel = 0
        for x in self.Tanks :
            totalFuel = totalFuel + x.fuel
        return totalFuel

    def debugComponentPrint(self):
        for x in self.components :
            print(x.get_vertices())

    def reset(self):
        self.destroyed = False
        self.position = (0,0)
        self.velocity = (0,0)
        self.angle = 0
        self._throttle = 0
        self._isAngleLocked = 0
        for c in self.components:
            print (c)
            c.reset()
