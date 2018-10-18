import pymunk as pm
import pygame as pg


class CelestialBody():
    def __init__(self, name_, space_, mass_, radius_, position_x, position_y, elasticity_, atmosphere_, bodytype):
        self.mass = mass_
        self.name = name_
        self.radius = radius_
        self.posx = position_x
        self.posy = position_y
        self.elasticity = elasticity_
        self.atmosphere = atmosphere_
        self.bodytype = bodytype_
        if self.bodytype == 0 :
            self.body = pm.Body(body_type=pm.Body.STATIC)
        else:
            self.body = pm.Body(body_type=pm.Body.KINEMATIC)
        self.shape = pm.Circle(self.body, self.radius)
        self.shape.mass = self.mass
        self.shape.elasticity = self.elasticity
        self.body.position = self.posx, self.posy
        space_.add(self.body, self.shape)





        