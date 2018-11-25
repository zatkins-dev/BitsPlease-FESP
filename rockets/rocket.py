from pymunk import Body as Body
import pygame as pg
from rockets import Thruster, RCSThruster, SAS, CommandModule, Tank
from audio import AudioManager



class Rocket(Body):
    """
    Extends pymunk.Body, and can hold and represent physics for the components of the rocket.
    """

    def __init__(self, components=[]):
        """
        Creates a Rocket with the given list of components.

        :param components:
        :type components: list(:py:class:`Component`)
        """
        Body.__init__(self)
        for c in components:
            c.body = self
        self._components = components
        self.angular_velocity_limit = 400000
        self.destroyed=False
        self.throttle = 0
        self.isAngleLocked = False

    @property
    def throttle(self):
        """
        The Throttle represents how much of the thrusters' power is being used, from 0 - 1.
        """
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
    def components(self):
        """
        A list of all of the individual :py:class:`Component` s that have been attatched to the rocket.
        The list is presented in the order of :py:class:`Thruster` s, :py:class:`SAS`, :py:class:`CommandModule` s, :py:class:`RCSThruster` s
        """
        return self.tanks + self.thrusters + self.SASmodules + self.commandModules + self.RCSThrusters

    @property
    def commandModules(self):
        """
        A list of all of the :py:class:`CommandModule` s that have been attatched to the rocket.
        """
        return list(filter(lambda c: isinstance(c, CommandModule), self._components))

    @property
    def thrusters(self):
        """
        A list of all of the :py:class:`Thruster` s - but not :py:class:`RCSThruster` s - that have been attatched to the rocket.
        """
        return list(filter(lambda c: isinstance(c, Thruster) and not isinstance(c, RCSThruster), self._components))

    @property
    def RCSThrusters(self):
        """
        A list of all of the :py:class:`RCSThruster` s that have been attatched to the rocket.
        """
        return list(filter(lambda c: isinstance(c, RCSThruster), self._components))

    @property
    def SASmodules(self):
        """
        A list of all of the :py:class:`SAS` Modules that have been attatched to the rocket.
        """
        return list(filter(lambda c: isinstance(c, SAS), self._components))

    @property
    def tanks(self):
        return list(filter(lambda c: isinstance(c, Tank), self._components))

    @property
    def isAngleLocked(self):
        """
        Represents whether or not the rocket is attempting to hold itself to a certain angle.
        """
        return self._isAngleLocked

    @isAngleLocked.setter
    def isAngleLocked(self, newAngleLocked):
        if len(self.SASmodules) is not 0:
            self._isAngleLocked = newAngleLocked
            for sas in self.SASmodules:
                sas.SASangle = self.angle
        else:
            self._isAngleLocked = False


    def tick(self, timescale):
        """
        Allows the rocket to perform its functions, checking input and applying thrust and rotation to itself.
        """
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
                module.holdAngle(timescale)
        else:
            for module in self.SASmodules:
                if currentKeys[pg.K_a]:
                    module.rotateCounterClockwise(timescale)
                if currentKeys[pg.K_d]:
                    module.rotateClockwise(timescale)

        # apply all of the thrusters, with the current throttle
        if self.throttle is not 0:
            for thruster in self.thrusters:
                if not thruster.destroyed:
                    thruster.applyThrust(self.throttle, timescale)



    def handleEvent(self, event):
        """
        A pygame event handler, currently only checks for the SAS angle-toggle key V
        """
        if event.type is pg.KEYDOWN:
            # new key has been pressed, place edge sensitive
            # commands in here, i.e. things that only run once
            # per key press
            if event.key is pg.K_v:  # Toggle SAS Lock
                self.isAngleLocked = not self.isAngleLocked


    def addComponent(self, c):
        """
        Add a new component to the rocket

        :param c: The component to add to the rocket
        :type c: :py:class:`Component`
        """

        c.body = self
        self._components.append(c)

    def removeComponent(self, c):
        """
        Removes a component from the rocket

        :param c: The component to remove from the rocket
        :type c: :py:class:`Component`
        """

        for x in self.components:
            if x.get_vertices() == c.get_vertices() :
                self._components.remove(x)


    def debugComponentPrint(self):
        """
        Prints out the verticies of all the components in this rocket.
        """
        for x in self.components :
            print(x.get_vertices())

    def reset(self):
        """
        Resets information about this rocket for purposes of restarting the simulation.
        This includes the destroyed flag, the position, velocity, angle, throttle, isAngleLocked,
        and also resets every component of the rocket.
        """
        self.destroyed = False
        self.position = (0,0)
        self.velocity = (0,0)
        self.angle = 0
        self._throttle = 0
        self._isAngleLocked = 0
        for c in self.components:
            c.reset()
