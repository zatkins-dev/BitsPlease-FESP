import pygame as pg
from component import Component

class SAS(Component):
    def __init__(self, body, vertices, SASforce, SASpower, angle, transform=None, radius=0):
        Component.__init__(self, body, vertices, transform, radius)
        self._SASangle = 0

        #SASforce: 0 is continue going straight, + turns the rocket left, - turns the rocket right
        #the greater the force the more the rocket turns
        self._SASforce = 0

        #SASpower: rate at which the rockets SASforce increments when given input from the user
        self._SASpower = 0.05


        self.leftKey = None
        self.rightKey = None

    @property
    def SASpower(self):
        return self._SASpower
    
    @SASpower.setter
    def SASpower(self, newPower):
        self._SASpower = newPower  


    @property
    def SASangle(self):
        return self._SASangle
    
    @SASangle.setter
    def SASangle(self, newAngle):
        self._SASangle = newAngle   

    @property
    def SASforce(self):
        return self._SASforce
    
    @SASforce.setter
    def SASforce(self, newForce):
        #give me all your SASs
        self._SASforce = newForce
