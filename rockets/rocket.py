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

    @property
    def thrusters(self):
        return list(filter(lambda c: isinstance(c, Thruster), self.components))

    @property
    def SASmodules(self):
        return list(filter(lambda c: isinstance(c, SAS), self.components))

    """def turn_SAS(self, k, coeffPower):
        #Turn SAS in direction determined by key k with power coeffPower.

        #Args:
         #   k (Int): Directional key in which to engage SAS.
          #  coeffPower (Float): Power of SAS to engage.

        
        for m in self.components:
            if not isinstance(m, SAS):
                continue
            else:
                if m.fuel > 0:
                    if m.leftKey == k:
                        self.angular_velocity += m.SASpower * coeffPower
                        m.fuel -= 1 * coeffPower

                    if m.rightKey == k:
                        self.angular_velocity -= m.SASpower * coeffPower
                        m.fuel -= 1 * coeffPower
                else:
                    # you silly goose
                    print('SAS module is out of fuel')

    def auto_SAS(self, targetAngle):
        #Engage SAS to sustain target angle

        #Args:
            #targetAngle (Float): Angle in radians to lock with SAS.

        
        if targetAngle > self.angle:
            self.turn_SAS(pg.K_a, 0.25)
        elif targetAngle < self.angle:
            self.turn_SAS(pg.K_d, 0.25)
        else:
            pass
            # do nothing, on course
    """

    def handleEvent(self, eventKey):
        if eventKey == pg.K_f : # Apply main thrust
            for ts in self.thrusters:
                # check to make sure this isn't an RCS thruster
                if not isinstance(ts, RCSThruster) and not ts.destroyed:
                    ts.applyThrust()
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
    
    #def getFuel():
        #adds all fuel stored in each fuel tank

    #def _decreaseFuel():

        #decreases fuel from first found fuel tank that contains fuel
    
