import pymunk as pm
import pygame as pg
from physics.collision import CT_CELESTIAL_BODY


class CelestialBody():
    """Wrapper class for celestial bodies, contains Body and Shape

    Args:
        name_ (String): Name of planet
        space_ (space): Space to embed planet in
        mass_ (Float): Mass of body
        radius_ (Float): Radius of circle
        position_x (Float): Center position x
        position_y (Float): Center position y
        elasticity_ (Float): Elasticity of shape
        atmosphere_ (Float): Damping coefficient for atmoshphere
        bodytype_ (Int): Type of body

    Attributes:
        mass (type): Mass of body
        name (type): Name of planet
        radius (type): Radius of circle
        posx (type): Center position x
        posy (type): Center position y
        elasticity (type): Elasticity of shape
        atmosphere (Float): Damping coefficient for atmoshphere
        bodytype (Int): Type of body
        body (Body): Body object of planet
        shape (Shape): Shape object of planet

    """
    def __init__(self, name_, space_, mass_, radius_, position_x, position_y,
                 elasticity_, atmosphere_color, atmosphere_height, bodytype_):
        self.name = name_
        self.atmosphereColor = atmosphere_color
        self.atmosphereHeight = atmosphere_height
        self.body = pm.Body(body_type=bodytype_)
        self.shape = pm.Circle(self.body, radius_)
        self.shape.friction = 0.80
        self.shape.mass = mass_
        self.shape.elasticity = elasticity_
        self.shape.collision_type = CT_CELESTIAL_BODY
        self.body.position = position_x, position_y
        space_.add(self.body, self.shape)