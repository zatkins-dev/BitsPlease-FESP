import math

class Physics(object):

    _GRAV_CONSTANT = 6.67384*(10**-11)

    @staticmethod
    #Calculates the force due to gravity between a body and a target
    #Assumes that the body and target have "mass" property and "position" tuple property
    def gravity(body, target):
        #First, find the distance between the body and the target
        #Then, Use that distance to calculate gravity
        dX = body.position[0] - target.position[0]
        dY = body.position[1] - target.position[1]

        rSquared = dX**2 + dY**2

        #Now, find force of gravity in the direction of R
        forceMagnitude = Physics._GRAV_CONSTANT * body.mass * target.mass / rSquared

        #Find the angle between these two so that this can be translated back to Cartesian Coords
        angle = math.atan2(dY, dX)

        fX = forceMagnitude * math.cos(angle)
        fY = forceMagnitude * math.sin(angle)

        return (fX, fY)

    @staticmethod
    #Calculates the net force due to gravity on some target from a list of bodies
    #Assumes that the body and target have "mass" property and "position" tuple property
    def netGravity(bodies, target):
        fX, fY = 0, 0
        for body in bodies:
            fX, fY = Physics.gravity(body, target)

        return (fX, fY)
