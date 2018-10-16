from pymunk import Body as Body
import pygame as pg
import pymunk as pm
from Rockets.component import Component
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
                self.apply_impulse_at_local_point(t.thrust(), (0, 0))
                

    def turn_SAS(self, k):
        for m in self.components:
            if not isinstance(m, SAS):
                continue
            else :    
                if m.leftKey == k:
                    m.SASforce = m.SASforce + m.SASpower
            
                if m.rightKey == k:
                    m.SASforce = m.SASforce - m.SASpower
                self.angular_velocity = m.SASforce
    def addComponent(self, c):
        self.components.append(c)
