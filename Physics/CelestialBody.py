import pymunk as pm
import pygame as pg


class CelestialBody():
    def __init__(self, name_, space_, mass_, radius_, position_x, position_y, elasticity_, atmosphere_, bodytype_):
        self.mass = mass_
        self.name = name_
        self.radius = radius_
        self.posx = position_x
        self.posy = position_y
        self.elasticity = elasticity_
        self.atmosphere = atmosphere_
        self.bodytype = bodytype_
        self.body = pm.Body(bodytype)
        self.shape = pm.Circle(self.body, self.radius)
        self.shape.mass = self.mass
        self.shape.elasticity = self.elasticity
        self.body.position = self.posx, self.posy
        space_.add(self.body, self.shape)





        