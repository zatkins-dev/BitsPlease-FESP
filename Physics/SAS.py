import pymunk.vec2d import vec2d
import pygame as pg
from component import Component

class SAS(Component):
    def __init__(self, body, vertices, SASdirection, SASforce, transform=None, radius=0):
        self._SASdirection = 0
        self._SASforce = 0
    
    def SAS_turning(self):
        return self._SASdirection * self._SASpower

    @property
    def SASdirection(self):
        return self._SASdirection
    
    @SASdirection.setter
    def SASdirection(self, newDir):
        self._SASdirection = newDir    

    @property
    def SASforce(self):
        return self._SASforce
    
    @SASforce.setter
    def SASforce(self, newForce):
        #give me all your SASs
        self._SASforce = newForce
