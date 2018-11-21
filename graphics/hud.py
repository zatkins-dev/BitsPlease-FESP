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
            *_font*:            The font used to draw text to the screen
            *_navBallRadius*:   The radius in pixels of the Hud's navball
            *_navBallSubRadius*:The radius in pixels of the small viewport
                                within the navball

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

        # define a surface to hold a navball
        self._navBallRadius = 75
        self._navBallSubRadius = 65

        self._hudForegroundColor = (75,75,75)
        self._hudBackgroundColor = (50,50,50)

        self._fontColor = (255,255,255)

        self._readableGreen = (0,175,0)

        if font is None:
            self._font = pg.font.SysFont("LucidaConsole", 12)
            self._bigFont = pg.font.SysFont("LucidaConsole", 16)
        else:
            self._font = font
            self._bigFont = font

    def _drawCompassLine(self, surface, angle, size, color=(255,255,255,255), innerRadius=None, outerRadius=None):
        if innerRadius is None or outerRadius is None:
            innerRadius = self._navBallSubRadius
            outerRadius = self._navBallRadius
        pg.draw.line(surface, color, 
            (outerRadius*math.cos(angle)+outerRadius, -1*outerRadius*math.sin(angle)+outerRadius),
            (innerRadius*math.cos(angle)+outerRadius, -1*innerRadius*math.sin(angle)+outerRadius), size)
        

    def _updateNavBall(self, rocket):
        # create a navball
        navBall = pg.Surface((2*self._navBallRadius, 2*self._navBallRadius), pg.SRCALPHA)
        navBall.fill((0,0,0,0))

        # draw a circle - the navball
        pg.draw.circle(navBall, self._hudForegroundColor, (self._navBallRadius,self._navBallRadius), self._navBallRadius)
        # draw some compass markings on the navball
        
        for i in range(12):
            # normal markings will have size 3
            size = 3
            if i%3 is 0:
                # markings on the poles (i=0,3,6,9) will have size 5
                size = 5
            self._drawCompassLine(navBall, i * math.pi / 6, size)

        # make a new surface to blit into the navball
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

        
        self._drawCompassLine(navBall, rocket.angle + math.pi/2, 5, (0,0,255))   # direction
        self._drawCompassLine(navBall, rocket.velocity.angle, 5, (0,255,0))      # velocity
        self._drawCompassLine(navBall, rocket.velocity.angle + math.pi, 5, (255,0,0))      # anti-velocity

        navBall.blit(subNavBall, (0,0))

        return navBall

    def _updateThrottle(self, rocket):
        # define some properties of the gauge
        gaugeSize = (30, 2*self._navBallRadius)
        gaugeBorder= 5

        # create the gauge, fill it, and draw a border
        gauge = pg.Surface(gaugeSize)
        gauge.fill(self._hudBackgroundColor)
        gauge.fill(self._hudForegroundColor, ((gaugeBorder,gaugeBorder),(gaugeSize[0]-2*gaugeBorder, gaugeSize[1]-2*gaugeBorder)))

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

        text = self._font.render("Throttle", True, self._fontColor)
        text = pg.transform.rotate(text, 90)
        gauge.blit(text, ((gaugeSize[0]/2)-(text.get_width()/8), (gaugeSize[1]/2)-(text.get_height()/2)))

        # draw one yellow mark to represent the current velocity
        drawMark(1 - rocket.throttle, 1, 3, (255,255,0))

        return gauge

    def _updateVelocity(self, rocket):
        velSurf = pg.Surface((220, 40))
        velSurf.fill(self._hudBackgroundColor)
        velSurf.fill(self._hudForegroundColor, (5,5,210,30))

        velString = "Velocity: "


        velNumber = rocket.velocity.length

        # find the number of spaces we need to pad the string with
        velString += " " * min(4, int(5-math.log10(velNumber)))
        velString += str(round(velNumber, 1))
        velString += "m/s"

        textSize = self._bigFont.size(velString)
        velTextPosition = ((velSurf.get_height()-textSize[1])/2 + textSize[0]/2, velSurf.get_height()/2)
        graph.drawTextCenter(velTextPosition, velString, self._bigFont, self._fontColor, velSurf)

        return velSurf

    def _updateSASFuel(self, rocket):
        # define some properties of the gauge
        gaugeSize = (30, 2*self._navBallRadius)
        gaugeBorder= 5

        # create the gauge, fill it, and draw a border
        gauge = pg.Surface(gaugeSize)
        gauge.fill(self._hudBackgroundColor)
        gauge.fill(self._hudForegroundColor, ((gaugeBorder,gaugeBorder),(gaugeSize[0]-2*gaugeBorder, gaugeSize[1]-2*gaugeBorder)))

        # find the maximum SAS fuel, and the current fuel
        maxFuel = 0
        curFuel = 0
        for module in rocket.SASmodules:
            maxFuel += module.maxFuel
            curFuel += module.fuel
        
        # ratio of fuel left
        fuelLeft = 0
        if maxFuel is not 0:
            fuelLeft = curFuel / maxFuel

        gauge.fill(self._readableGreen, ( # fill a rect that is equal to the proportion of the gauge the fuel will fill
            (gaugeBorder, gaugeBorder + (gaugeSize[1] - 2 * gaugeBorder) * (1 - fuelLeft)),
            (gaugeSize[0] - 2 * gaugeBorder, (gaugeSize[1] - 2 * gaugeBorder) * fuelLeft)
        ))

        text = self._font.render("SAS Fuel", True, self._fontColor)
        text = pg.transform.rotate(text, 90)
        gauge.blit(text, ((gaugeSize[0]/2)-(text.get_width()/2), (gaugeSize[1]/2)-(text.get_height()/2)))

        return gauge

    def _updateThrusterFuel(self, rocket):
        thrusters = rocket.thrusters
        thrusters.sort(key=lambda x: x.maxFuel)

        gaugeSize = (2*self._navBallRadius, 25)
        gaugeBorder= 5

        overallSize = (gaugeSize[0], gaugeSize[1] * len(thrusters) + gaugeBorder)

        gauge = pg.Surface(overallSize)
        gauge.fill(self._hudBackgroundColor)

        i = 0

        for thruster in thrusters:
            innerPos = (gaugeBorder, i * gaugeSize[1] + gaugeBorder)
            gauge.fill(self._hudForegroundColor, (
                innerPos, 
                (gaugeSize[0] - 2*gaugeBorder, gaugeSize[1] - gaugeBorder)
            ))

            fuelLeft = thruster.fuel / thruster.maxFuel

            gauge.fill(self._readableGreen, (
                innerPos,
                (fuelLeft * (gaugeSize[0] - 2*gaugeBorder), gaugeSize[1] - gaugeBorder)
            ))

            textPos = (innerPos[0] + (gaugeSize[0] - 2*gaugeBorder)/2, innerPos[1] + (gaugeSize[1] - gaugeBorder)/2)

            graph.drawTextCenter(textPos, type(thruster).__name__, self._font, self._fontColor, gauge)

            i += 1

        return gauge

    def _updateSASIndicator(self, rocket):
        indicatorSize = (35,30)
        indicatorBorder = 5
        indicator = pg.Surface(indicatorSize)

        indicator.fill(self._hudBackgroundColor)

        # find the correct interior color: red if off, green if on
        color = (255,0,0)
        if rocket.isAngleLocked:
            color = self._readableGreen

        # fill the interior
        indicator.fill(color, ((0, indicatorBorder), (indicatorSize[0] - 1 * indicatorBorder, indicatorSize[1] - 2 * indicatorBorder)))

        graph.drawTextCenter(((indicatorSize[0]-indicatorBorder)/2, indicatorSize[1]/2), "SAS", self._font, self._fontColor, indicator)

        return indicator
            


    def updateHUD(self, rocket):
        """
            Update the values that are displayed on the screen,
            then draw the text to the screen

            **Preconditions**:
                None.

            **Postconditions**:
                None.

            **Returns**: None.
        """
        
        navBallPos = (int(pg.display.get_surface().get_width()/2 - self._navBallRadius), int(pg.display.get_surface().get_height()-2*self._navBallRadius))
        pg.display.get_surface().blit(self._updateNavBall(rocket), navBallPos)

        throttleGauge = self._updateThrottle(rocket)
        throttlePos = (navBallPos[0] - throttleGauge.get_width(), navBallPos[1])
        pg.display.get_surface().blit(self._updateThrottle(rocket), throttlePos)

        velocity = self._updateVelocity(rocket)
        velocityPos = (throttlePos[0]-velocity.get_width(), pg.display.get_surface().get_height()-velocity.get_height())
        pg.display.get_surface().blit(self._updateVelocity(rocket), velocityPos)

        sasFuel = self._updateSASFuel(rocket)
        sasFuelPos = (navBallPos[0] + 2*self._navBallRadius, navBallPos[1])
        pg.display.get_surface().blit(sasFuel, sasFuelPos)

        sasIndicator = self._updateSASIndicator(rocket)
        sasIndicatorPos = (sasFuelPos[0] + sasFuel.get_width(), pg.display.get_surface().get_height() - sasIndicator.get_height())
        pg.display.get_surface().blit(sasIndicator, sasIndicatorPos)

        thrusterFuel = self._updateThrusterFuel(rocket)
        thrusterFuelPos = (pg.display.get_surface().get_width() - thrusterFuel.get_width(), pg.display.get_surface().get_height() - thrusterFuel.get_height())
        pg.display.get_surface().blit(thrusterFuel, thrusterFuelPos)

