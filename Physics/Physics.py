import math

class Physics(object):

    _GRAV_CONSTANT = 6.67384*(10**-11)

    @staticmethod
    #Calculates the force due to gravity between a body and a target
    #Assumes that the body and target have "mass" property and "position" tuple property
    def gravity(shape, body, target):
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
    #Calculates the net force due to gravity on some target from a list of bodies
    #Assumes that the body and target have "mass" property and "position" tuple property
    def netGravity(bodies, shapes, target):
        fX, fY = 0, 0
        for body, shape in zip(bodies, shapes):
            newVec = Physics.gravity(shape, body, target)
            fX += newVec[0]
            fY += newVec[1]

        return (fX, fY)
