from Rockets.component import Component


class SAS(Component):
    """Short summary.

    Args:
        body (Body): Rocket body to attach to
        vertices (List(Vec2d)): Vertices of Poly shape
        SASpower (Float): rotation rate of the rocket from the SAS module
        angle (Float): lock angle for the SAS
        transform (Transform): Description of parameter `transform`.
        radius (Float): Description of parameter `radius`.

    Attributes:
        _SASangle (Float): lock angle for the SAS
        _SASpower (Float): rotation rate of the rocket from the SAS module
        leftKey (Int): Description of parameter `leftKey`.
        rightKey (Int): Description of parameter `rightKey`.
        fuel (Int): Description of parameter `fuel`.

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

    @property
    def SASpower(self):
        return self._SASpower

    @SASpower.setter
    def SASpower(self, newPower):
        self._SASpower = newPower

    @property
    def SASangle(self):
        return self._SASangle

    @SASangle.setter
    def SASangle(self, newAngle):
        self._SASangle = newAngle
