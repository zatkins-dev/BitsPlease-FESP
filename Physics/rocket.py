from pymunk import Body as Body
import pygame as pg
import pymunk as pm
from component import Component
from thruster import Thruster


class Rocket(Body):
    def __init__(self, components=[]):
        Body.__init__(self)
        for c in components:
            c.body = self
        self.components = components
        self.thrusters = filter(lambda c: type(c) == Thruster, self.components)
        self.rotationLeftKey = pg.K_a
        self.rotationRightKey = pg.K_d

    def thrust(self, k):
        for t in self.components:
            if t.key is None:
                continue
            if t.key == k:
                self.apply_impulse_at_local_point(t.thrust(), (0, 0))

    def rotate(self, k):
        if self.rotationLeftKey == k :
            self.angle = self.angle + 0.05
            self.torque = self.torque + 1000
        if self.rotationRightKey == k :
            self.angle = self.angle - 0.05
            self.torque = self.torque -1000

    def addComponent(self, c):
        self.components.append(c)
