import pymunk as pm
import pygame as pg
from physics.collision import CT_CELESTIAL_BODY


class CelestialBody():
    """
    Wrapper class for celestial bodies, contains Body and Shape
    """

    def __init__(self, name_, space_, mass_, radius_, position_,
                 elasticity_, atmosphere_color, atmosphere_height, bodytype_):
        """
        Creates the celestial body.

        :param str name_: The name to give the planet
        :param space_: The space to add the planet to
        :type space_: :py:class:`pymunk.Space`
        :param float mass_: The mass of the planet
        :param float radius_: The radius of the planet
        :param position_: The (x,y) position of the center of the planet
        :type position_: tuple(float, float)
        :param float elasticity_: The elasticity of the planet in collisions.
        :param atmosphere_color: The color of the planet's sky.
        :type atmosphere_color: tuple(int, int, int)
        :param float atmosphere_height: The height of the planet's atmosphere.
        :param int bodytype_: The type of body 

        """
        #: Planet name
        self.name = name_
        #: Color of planet atmosphere
        self.atmosphereColor = atmosphere_color
        #: Height of planet atmosphere
        self.atmosphereHeight = atmosphere_height
        #: :py:class:`pymunk.Body` of the celestial body
        #: Stores :py:class:`pymunk.vec2d.Vec2d` position
        self.body = pm.Body(body_type=bodytype_)
        #: :py:class:`pymunk.Circle` of the celestial body
        #: Stores: :py:class:`float` friction, :py:class:`float` mass,
        #: :py:class:`float` elasticity, :py:class:`int` collision type
        self.shape = pm.Circle(self.body, radius_)
        self.shape.friction = 0.80
        self.shape.mass = mass_
        self.shape.elasticity = elasticity_
        self.shape.collision_type = CT_CELESTIAL_BODY
        self.body.position = position_
        space_.add(self.body, self.shape)