import math

class Physics(object):
    """
    Physics is a utility class that is used to encapsulate different physics
    functions to be used in our simulation.
    Currently, it only handles finding the force due to gravity

    **Class Variables**:
        *_GRAV_CONSTANT*:       float The gravitational constant
    """

    _GRAV_CONSTANT = 6.67384*(10**-11)

    @staticmethod
    def gravity(shape, body, target):
        """
        Calculate gravitational force between a target and body/shape pair.

        **Args**:
                *shape*:    pymunk.Shape The shape of the planet the use as
                                         the gravitational source

                *body*:     pymunk.Body The Body of the planet to use as the
                                        gravitational source

                *target*:   Rocket The object that gravity will be affecting

        **Preconditions**:
                Shape and Target both contain a mass property, and Body and
                Target both contain a position property

        **Postconditions**:
                None.

        **Returns**: Return the force due to gravity in vector (tuple) form.
        """
        #First, find the distance between the body and the target
        #Then, Use that distance to calculate gravity
        dX = body.position[0] - target.position[0]
        dY = body.position[1] - target.position[1]

        rSquared = dX**2 + dY**2

        #Now, find force of gravity in the direction of R
        forceMagnitude = Physics._GRAV_CONSTANT * shape.mass * target.mass / rSquared

        #Find the angle between these two so that this can be translated back to Cartesian Coords
        angle = math.atan2(dY, dX)

        fX = forceMagnitude * math.cos(angle)
        fY = forceMagnitude * math.sin(angle)

        return (fX, fY)

    @staticmethod
    def netGravity(bodies, shapes, target):
        """
        Calculate gravitational force between a target and some other bodies.

        **Args**:
                *shapes*: list[pymunk.Shape] The shapes of the planets the
                                             use as the gravitational sources

                *body*: list[pymunk.Body] The Bodies of the planets to use
                                              as the gravitational sources

                *target*: Rocket The object that gravity will be affecting

        **Preconditions**:
                Elements in Shapes and Target contain a mass property,
                and elements in Body and Target contain a position property

        **Postconditions**:
                None.

        **Returns**: Tuple(float, float) The net gravity vector
        """
        fX, fY = 0, 0
        for body, shape in zip(bodies, shapes):
            newVec = Physics.gravity(shape, body, target)
            fX += newVec[0]
            fY += newVec[1]

        return (fX, fY)
