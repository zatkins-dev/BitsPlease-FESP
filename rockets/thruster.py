from pymunk.vec2d import Vec2d
from rockets import Component


class Thruster(Component):
    """Thruster component for rocket. Provides encapsulation for
       thrust direction and magnitude. Must be attached to a body.

    Args:
        body (pymunk.Body): body thruster is attached to.
        vertices (list(pymunk.Vec2d)): vertices of polygon shape.
        thrustVector (pymunk.Vec2d): direction of thrust (relative to Rocket).
        netThrust (float): magnitude of thrust.
        transform (float): transformation to be applied to shape.
        radius (float): edge radius of shape (smoothing).

    Attributes:
        _thrustVector (pymunk.Vec2d): direction of thrust (relative to Rocket).
        _thrustForce (float): magnitude of thrust.
        fuel (int): current thruster fuel.

    """

    def __init__(self, body, vertices, thrustVector,
                 netThrust, transform=None, radius=0):
        Component.__init__(self, body, vertices, transform, radius)
        self._thrustVector = Vec2d(thrustVector)
        self._thrustForce = netThrust
        self.fuel = 40000

    def thrust(self):
        """Gets the scaled thrust vector for application of forces

        Returns:
            pymunk.Vec2d: Scaled thrust vector.

        """
        return self.thrustForce * self.thrustVector

    @property
    def thrustForce(self):
        """Magnitude of thrust

        Returns:
            float: thrust magnitude.

        """
        return self._thrustForce

    @thrustForce.setter
    def thrustForce(self, netForce):
        self._thrustForce = netForce

    @property
    def thrustVector(self):
        """Direction of thrust

        Returns:
            pymunk.Vec2d: direction of thrust adjusted for rocket rotation.

        """
        if self._thrustVector is None:
            self._thrustVector = Vec2d(0, 1)
        tVect = Vec2d(self._thrustVector)
        tVect.cpvrotate(self.body.rotation_vector)
        return tVect

    @thrustVector.setter
    def thrustVector(self, v):
        self._thrustVector = Vec2d(v).normalized()
