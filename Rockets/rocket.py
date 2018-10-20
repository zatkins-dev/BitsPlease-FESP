from pymunk import Body as Body
import pygame as pg
from Rockets.thruster import Thruster
from Rockets.SAS import SAS


class Rocket(Body):
    def __init__(self, components=[]):
        Body.__init__(self)
        for c in components:
            c.body = self
        self.components = components
        self.thrusters = filter(lambda c: type(c) == Thruster, self.components)
        self.SASmodules = filter(lambda c: type(c) == SAS, self.components)
        self.angular_velocity_limit = 400000

    def thrust(self, k):
        for t in self.components:
            if t.key is None:
                continue
            if t.key == k:
                if t.fuel > 0:
                    self.apply_impulse_at_local_point(t.thrust(), (0, 0))
                    t.fuel -= 1

    def turn_SAS(self, k, coeffPower):
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
        if targetAngle > self.angle:
            self.turn_SAS(pg.K_a, 0.25)
        elif targetAngle < self.angle:
            self.turn_SAS(pg.K_d, 0.25)
        else:
            pass
            # do nothing, on course

    def addComponent(self, c):
        self.components.append(c)
