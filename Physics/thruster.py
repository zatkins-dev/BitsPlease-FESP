from pymunk.vec2d import Vec2d
import pygame as pg
from component import Component


class Thruster(Component):
    def __init__(self, body, vertices, thrustVector, netThrust, transform=None, radius=0):
        Component.__init__(self, body, vertices, transform, radius)
        self._thrustVector = Vec2d(thrustVector)
        self._thrustForce = netThrust
        
    def thrust(self):
        return self.thrustForce * self.thrustVector

    @property
    def thrustForce(self):
        return self._thrustForce

    @thrustForce.setter
    def thrustForce(self, netForce):
        self._thrustForce = netForce

    @property
    def thrustVector(self):
        if self._thrustVector is None:
            self._thrustVector = Vec2d(0, 1)
        tVect = Vec2d(self._thrustVector)
        tVect.cpvrotate(self.body.rotation_vector)
        return tVect

    @thrustVector.setter
    def thrustVector(self, v):
        self._thrustVector = Vec2d(v).normalized()
