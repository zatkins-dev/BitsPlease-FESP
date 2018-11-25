import math
from pymunk.vec2d import Vec2d

class Physics(object):
    """
    Physics is a utility class that is used to encapsulate different physics
    functions to be used in our simulation.
    Currently, it only handles finding the acceleration due to gravity
    """

    #: The Gravitational Constant
    _GRAV_CONSTANT = 6.67384*(10**-11)

    @staticmethod
    def gravity(celestialBody, targetPosition):
        """
        Calculate gravitational acceleration on target by body/shape pair.

        :param celestialBody: The planet to use as the gravitational source
        :type celestialBody: :py:class:`CelestialBody`
        :param targetPosition: The (x,y) position of the target
        :type targetPosition: :py:class:`pymunk.vec2d.Vec2d`
        :returns: Acceleration vector
        :rtype: :py:class:`pymunk.vec2d.Vec2d`
        """

        #First, find the distance between the body and the target
        #Then, Use that distance to calculate gravity
        dPos = celestialBody.body.position - targetPosition

        rSquared = dPos.get_length_sqrd()

        #Now, find acceleration due to gravity in the direction of R
        accelMagnitude = Physics._GRAV_CONSTANT * celestialBody.shape.mass / rSquared

        return accelMagnitude*dPos.normalized()

    @staticmethod
    def netGravity(celestialBodies, targetPosition):
        """
        Calculate gravitational acceleration on a target by several bodies.

        :param celestialBodies: The planets to use as the gravitational sources
        :type celestialBodies: [:py:class:`.CelestialBody`]
        :param targetPosition: The (x,y) position of the target
        :type targetPosition: :py:class:`pymunk.vec2d.Vec2d`
        :returns: Acceleration vector
        :rtype: :py:class:`pymunk.vec2d.Vec2d`
        """
        accel = Vec2d(0,0)
        for celestialBody in celestialBodies:
            accel += Physics.gravity(celestialBody, targetPosition)
        return accel
