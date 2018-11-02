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
    def gravity(celestialBody, target):
        """
        Calculate gravitational force between a target and body/shape pair.

        **Args**:
                *body*:     pymunk.Body The planet to use as the
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
        dX = celestialBody.body.position[0] - target.position[0]
        dY = celestialBody.body.position[1] - target.position[1]

        rSquared = target.position.get_distance(celestialBody.body.position)**2
        #Now, find force of gravity in the direction of R
        forceMagnitude = Physics._GRAV_CONSTANT * celestialBody.shape.mass / rSquared

        #Find the angle between these two so that this can be translated back to Cartesian Coords
        angle = math.atan2(dY, dX)

        fX = forceMagnitude * math.cos(angle)
        fY = forceMagnitude * math.sin(angle)
        # if celestialBody.name == "earth":
            # print("Mass of earth:\n\t {0}\n r^2:\n\t {1}\nNet Acceleration\n\t {2}\nAcceleration vector:\n\t {3}".format(celestialBody.shape.mass, rSquared, forceMagnitude, (fX,fY)))

        return (fX, fY)

    @staticmethod
    def netGravity(celestialBodies, target):
        """
        Calculate gravitational force between a target and some other bodies.

        **Args**:
                *celestialBodies*: list[celesitalbody] The planets to use
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
        for celestialBody in celestialBodies:
            newVec = Physics.gravity(celestialBody, target)
            fX += newVec[0]
            fY += newVec[1]

        return (fX, fY)
