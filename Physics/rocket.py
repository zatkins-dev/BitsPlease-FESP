from pymunk import Body as Body
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

    def thrust(self, k):
        for t in self.components:
            if t.key is None:
                continue
            if t.key == k:
                self.apply_force_at_local_point(t.thrust(), (0, 0))

    def addComponent(self, c):
        self.components.append(c)
