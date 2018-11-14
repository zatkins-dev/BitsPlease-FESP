from rockets import Component


class SAS(Component):
    """SAS component for rocket. Provides encapsulation for
       SAS autonomous angle and magnitude of SAS force.
       Must be attached to a body.

    Args:
        body (Body): Rocket body to attach to
        vertices (List(Vec2d)): Vertices of Poly shape
        SASpower (Float): Rotation rate of the rocket from the SAS module
        angle (Float): Lock angle for the SAS
        transform (Transform): Transformation to apply to shape
        radius (Float): Edge radius of shape for smoothing

    Attributes:
        _SASangle (Float): Lock angle for the SAS
        _SASpower (Float): Rotation rate of the rocket from the SAS module
        leftKey (Int): Key to activate left SAS.
        rightKey (Int): Key to activate right SAS.
        fuel (Int): Number game ticks of remaining fuel.

    """

    def __init__(self, body, vertices, SASpower, angle,
                 transform=None, radius=0):
        Component.__init__(self, body, vertices, transform, radius)
        self._SASangle = 0

        # SASpower: rotation of the rocket from the SAS module
        self._SASpower = 0.05

        self.leftKey = None
        self.rightKey = None

        # this number should probably be adjusted
        self.fuel = 2000

        self.transform = transform
    @property
    def SASpower(self):
        """Rotation rate of the rocket from the SAS module

        Returns:
            Float: Value of _SASpower

        """
        return self._SASpower

    @SASpower.setter
    def SASpower(self, newPower):
        """Setter for SASpower

        Args:
            newPower (Float): New value for _SASpower

        """
        self._SASpower = newPower

    @property
    def SASangle(self):
        """Lock angle in radians for the SAS

        Returns:
            Float: Value of _SASangle

        """
        return self._SASangle

    @SASangle.setter
    def SASangle(self, newAngle):
        """Setter for _SASangle

        Args:
            newAngle (Float): New value for _SASangle

        """
        self._SASangle = newAngle
