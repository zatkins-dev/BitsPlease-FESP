import math

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
        Calculate gravitational force between a target and body/shape pair.

        :param celestialBody: The planet to use as the gravitational source
        :type celestialBody: :py:class:`CelestialBody`
        :param targetPosition: The (x,y) position of the target
        :type targetPosition: tuple(float, float)
        """

        #First, find the distance between the body and the target
        #Then, Use that distance to calculate gravity
        dX = celestialBody.body.position[0] - targetPosition[0]
        dY = celestialBody.body.position[1] - targetPosition[1]

        rSquared = (dX**2 + dY**2)

        #Now, find acceleration due to gravity in the direction of R
        AccelMagnitude = Physics._GRAV_CONSTANT * celestialBody.shape.mass / rSquared

        #Find the angle between these two so that this can be translated back to Cartesian Coords
        angle = math.atan2(dY, dX)

        fX = AccelMagnitude * math.cos(angle)
        fY = AccelMagnitude * math.sin(angle)

        return (fX, fY)

    @staticmethod
    def netGravity(celestialBodies, targetPosition):
        """
        Calculate gravitational force between a target and some other bodies.

        :param celestialBodies: The planets to use as the gravitational sources
        :type celestialBodies: list(:py:class:`CelestialBody`)
        :param targetPosition: The (x,y) position of the target
        :type targetPosition: tuple(float, float)
        """
        fX, fY = 0, 0
        for celestialBody in celestialBodies:
            newVec = Physics.gravity(celestialBody, targetPosition)
            fX += newVec[0]
            fY += newVec[1]

        return (fX, fY)
