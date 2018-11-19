import pygame as pg
from graphics import Graphics as graph
from rockets import Thruster
from rockets import SAS


class HUD():
    """
        HUD holds diagnostic info and prints values to the screen.

        **Instance Variables**:
            *_xPosition*:       float Holds the x position of the rocket.
                                      This value is printed to the screen.
            *_yPosition*:       float Holds the y position of the rocket.
                                      This value is printed to the screen.
            *_positionDegree*:  float The direction of the nose of the rocket.
            *_velocityMag*:     float The velocity magnitude of the rocket.
            *_velocityDegree*:  float The direction of rocket velocity
            *_accelerationMag*: float The magnitude of gravity on the rocket.
            *_accelerationDegree*: float The direction gravity on the rocket.
            *_thrusters*:       list[Thruster] The thrusters of the rocket
            *_SASmodules*:      list[SAS] The SAS modules of the rocket.
            *_font*:            The font used to draw text to the screen
    """

    def __init__(self, font=None):
        """
            Creates a new headsUpDisplay object, and initiailzes values to 0

            **Preconditions**:
                None.

            **Postconditions**:
                None.

            **Returns**: A headsUpDisplay object.
        """
        self._xPosition = 0
        self._yPosition = 0
        self._positionDegree = 0
        self._velocityMag = 0
        self._velocityDegree = 0
        self._accelerationMag = 0
        self._accelerationDegree = 0
        self._thrusters = None
        self._SASmodules = None

        if font is None:
            self._font = pg.font.SysFont("Futura", 20)
        else:
            self._font = font

    def updateHUD(self, x, y, pDeg, vMag, vDeg, aMag, aDeg, components, fps):
        """
            Update the values that are displayed on the screen,
            then draw the text to the screen

            **Preconditions**:
                None.

            **Postconditions**:
                None.

            **Returns**: None.
        """
        self._xPosition = x
        self._yPosition = y
        self._positionDegree = pDeg
        self._velocityMag = vMag
        self._velocityDegree = vDeg
        self._accelerationMag = aMag
        self._accelerationDegree = aDeg
        self.thrusters = filter(lambda c: isinstance(c, Thruster) and c.fuel != 0, components)
        self.SASmodules = filter(lambda c: isinstance(c, SAS), components)

        graph.drawText((10, 10), "X Position: "
                       + str("{:10.4f}".format(self._xPosition))
                       + " m", self._font, (255, 0, 0))
        graph.drawText((10, 30), "Y Position: "
                       + str("{:10.4f}".format(self._yPosition))
                       + " m", self._font, (255, 0, 0))
        graph.drawText((10, 50), "Nose Degree: "
                       + str("{:10.4f}".format(self._positionDegree))
                       + " degrees", self._font, (255, 0, 0))
        graph.drawText((10, 70), "Velocity Magnitude: "
                       + str("{:10.4f}".format(self._velocityMag))
                       + " m/s", self._font, (255, 0, 0))
        graph.drawText((10, 90), "Velocity Degree: "
                       + str("{:10.4f}".format(self._velocityDegree))
                       + " degrees", self._font, (255, 0, 0))
        graph.drawText((10, 110), "Acceleration Magnitude: "
                       + str("{:10.4f}".format(self._accelerationMag))
                       + " m/s^2", self._font, (255, 0, 0))
        graph.drawText((10, 130), "Acceleration Degree: "
                       + str("{:10.4f}".format(self._accelerationDegree))
                       + " degrees", self._font, (255, 0, 0))

        numThruster = 0
        for thruster in self.thrusters:
            numThruster = numThruster + 1
            graph.drawText((10, 130 + numThruster*20), "Thruster Module "
                           + str(numThruster) + " Fuel Remaining: "
                           + str("{:10.0f}".format(thruster.fuel))
                           + " Liters", self._font, (255, 0, 0))

        numSAS = 0
        for sas in self.SASmodules:
            numSAS = numSAS + 1
            graph.drawText((10, 130 + numThruster*20 + numSAS*20),
                           "SAS Module " + str(numSAS) + " Fuel Remaining: "
                           + str("{:10.0f}".format(sas.fuel))
                           + " Liters", self._font, (255, 0, 0))

        graph.drawText((10, 150 + numThruster*20 + numSAS*20),
                       "FPS: "
                       + "{:0.3f}".format(fps), self._font, (255, 0, 0))
