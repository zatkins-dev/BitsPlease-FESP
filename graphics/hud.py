import pygame as pg
import pymunk as pm
import math
from graphics import Graphics as graph
from rockets import Thruster
from rockets import SAS
from graphics.drawer import Drawer


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

        # define a surface to hold a navball
        self._navBallRadius = 75
        self._navBallSubRadius = 65
        self._navBall = pg.Surface((2*self._navBallRadius, 2*self._navBallRadius), pg.SRCALPHA)
        self._navBall.fill((0,0,0,0))

        # draw a circle - the navball
        pg.draw.circle(self._navBall, (75,75,75,255), (self._navBallRadius,self._navBallRadius), self._navBallRadius)
        # draw some compass markings on the navball
        self._drawCompassLine(self._navBall, 0, 5)
        self._drawCompassLine(self._navBall, math.pi/2, 5)
        self._drawCompassLine(self._navBall, math.pi/4, 3)
        self._drawCompassLine(self._navBall, 3*math.pi/4, 3)
        self._drawCompassLine(self._navBall, math.pi, 3)
        self._drawCompassLine(self._navBall, 5*math.pi/4, 3)
        self._drawCompassLine(self._navBall, 3*math.pi/2, 3)
        self._drawCompassLine(self._navBall, 7*math.pi/4, 3)
        self._drawCompassLine(self._navBall, 2*math.pi, 3)

        if font is None:
            self._font = pg.font.SysFont("LucidaConsole", 12)
        else:
            self._font = font

    def _drawCompassLine(self, surface, angle, size, color=(255,255,255,255), innerRadius=None, outerRadius=None):
        if innerRadius is None or outerRadius is None:
            innerRadius = self._navBallSubRadius
            outerRadius = self._navBallRadius
        pg.draw.line(surface, color, 
            (outerRadius*math.cos(angle)+outerRadius, -1*outerRadius*math.sin(angle)+outerRadius),
            (innerRadius*math.cos(angle)+outerRadius, -1*innerRadius*math.sin(angle)+outerRadius), size)
        

    def _updateNavBall(self, rocket):
        # make a copy of the original navBall to return
        newNavBall = self._navBall.copy()
        # make a new surface to blit into the navball copy
        subNavBall = pg.Surface((2*self._navBallRadius, 2*self._navBallRadius), pg.SRCALPHA)
        
        # the new surface will contain a darker inner circle for the navball
        # this circle will contain a viewport for the rocket
        pg.draw.circle(subNavBall, (30,30,30,255), (self._navBallRadius, self._navBallRadius), self._navBallSubRadius)
        # create a mask, so we can sort out which parts are transparent when we blit the rocket
        mask = pg.mask.from_surface(subNavBall)

        # draw the rocket onto the new subNavball
        # set the zoom level to 1, and then restore afterwards
        preZoom = Drawer._zoom
        Drawer._zoom = 1
        Drawer.drawMultiple(subNavBall, rocket.components, Drawer.getOffset(subNavBall, rocket))
        Drawer._zoom = preZoom

        # for any place where the mask showed a transparency, we should set to be transparent again
        # this gives the look of a circular viewport
        for x in range(subNavBall.get_width()):
            for y in range(subNavBall.get_height()):
                if mask.get_at((x,y)) is 0:
                    subNavBall.set_at((x,y), (0,0,0,0))

        
        self._drawCompassLine(newNavBall, rocket.angle + math.pi/2, 5, (0,0,255))
        self._drawCompassLine(newNavBall, rocket.velocity.angle, 5, (0,255,0))

        newNavBall.blit(subNavBall, (0,0))

        return newNavBall

    def _updateThrottle(self, rocket):
        # define some properties of the gauge
        gaugeSize = (30, 2*self._navBallRadius)
        gaugeBorder= 5

        # create the gauge, fill it, and draw a border
        gauge = pg.Surface(gaugeSize)
        gauge.fill((50,50,50))
        gauge.fill((75,75,75), ((gaugeBorder,gaugeBorder),(gaugeSize[0]-2*gaugeBorder, gaugeSize[1]-2*gaugeBorder)))

        # a small helper function to draw tick marks on the inside of the gauge
        def drawMark(y, width, size, color=(255,255,255)):
            pg.draw.line(gauge, color, 
                (gaugeBorder, y*(gaugeSize[1]-2*gaugeBorder)+gaugeBorder),
                (width*(gaugeSize[0]-2*gaugeBorder)+gaugeBorder, y*(gaugeSize[1]-2*gaugeBorder)+gaugeBorder), size)

        # draw tick marks at ever eighth
        for i in range(1,8):
            width = .25
            size = 1
            if i % 2 is 0:
                width = .5
                size = 3
            drawMark(i/8, width, size)

        text = self._font.render("Throttle", True, (255,255,255))
        text = pg.transform.rotate(text, 90)
        gauge.blit(text, ((gaugeSize[0]/2)-(text.get_width()/8), (gaugeSize[1]/2)-(text.get_height()/2)))

        # draw one yellow mark to represent the current velocity
        drawMark(1 - rocket.throttle, 1, 3, (255,255,0))

        return gauge

    def updateHUD(self, rocket, aMag, aDeg, fps):
        """
            Update the values that are displayed on the screen,
            then draw the text to the screen

            **Preconditions**:
                None.

            **Postconditions**:
                None.

            **Returns**: None.
        """
        self._xPosition = rocket.position[0]
        self._yPosition = rocket.position[1]
        self._positionDegree = (math.degrees(rocket.angle)+90) % 360
        self._velocityMag = rocket.velocity.length
        self._velocityDegree = rocket.velocity.angle_degrees % 360
        self._accelerationMag = aMag
        self._accelerationDegree = aDeg
        self.thrusters = rocket.thrusters
        self.SASmodules = rocket.SASmodules

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

        
        navBallPos = (int(pg.display.get_surface().get_width()/2 - self._navBallRadius), int(pg.display.get_surface().get_height()-2*self._navBallRadius))
        pg.display.get_surface().blit(self._updateNavBall(rocket), navBallPos)

        throttleGauge = self._updateThrottle(rocket)
        throttlePos = (navBallPos[0] - throttleGauge.get_width(), navBallPos[1])
        pg.display.get_surface().blit(self._updateThrottle(rocket), throttlePos)

        
