import pygame as pg
import pymunk as pm
import math
from graphics import Graphics as graph
from rockets import Thruster
from rockets import SAS
from physics import TimeScale
from graphics.drawer import Drawer


class HUD():
    """
        HUD holds diagnostic info and prints values to the screen.

        :param _font: The font used to draw text to the screen
        :type _font: :py:class:`pygame.Font`
        :param int _navBallRadius: The radius in pixels of the Hud's navball
        :param int _navBallSubRadius: The radius in pixels of the small viewport within the navball

    """

    def __init__(self):
        """
            creates a new HUD object 
        """

        # define a surface to hold a navball
        self._navBallRadius = 75
        self._navBallSubRadius = 65

        self._hudForegroundColor = (75,75,75)
        self._hudBackgroundColor = (50,50,50)

        self._fontColor = (255,255,255)

        self._readableGreen = (0,175,0)

        self._font = pg.font.SysFont("LucidaConsole", 12)
        self._bigFont = pg.font.SysFont("LucidaConsole", 16)

    def _drawCompassLine(self, surface, angle, size, color=(255,255,255,255), innerRadius=None, outerRadius=None):
        """
        Helper function to draw a line along the normal/radius of a circle
        """
        if innerRadius is None or outerRadius is None:
            innerRadius = self._navBallSubRadius
            outerRadius = self._navBallRadius
        pg.draw.line(surface, color, 
            (outerRadius*math.cos(angle)+outerRadius, -1*outerRadius*math.sin(angle)+outerRadius),
            (innerRadius*math.cos(angle)+outerRadius, -1*innerRadius*math.sin(angle)+outerRadius), size)
        

    def _updateNavBall(self, rocket):
        """
        Creates and returns a navball, containing directional information to a pygame Surface.
        
        :param rockets.rocket rocket: The rocket who's information to use.
        """
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
        preZoom = Drawer.zoom.zoom
        Drawer.zoom.reset()
        Drawer.drawMultiple(subNavBall, rocket.components, Drawer.getOffset(subNavBall, rocket))
        Drawer.zoom._set_zoom(preZoom)

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
        """
        Creates and returns a surface containing the throttle of the provided rocket.
        
        :param rockets.rocket rocket: The rocket who's throttle to use.
        """

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
        """
        Creates and returns a surface containing the velocity of the provided rocket.
        
        :param rockets.rocket rocket: The rocket who's velocity to use.
        """

        velSurfSize = (215,40)
        velSurfBorder = 5
        velSurf = pg.Surface(velSurfSize)
        velSurf.fill(self._hudBackgroundColor)
        velSurf.fill(self._hudForegroundColor, (velSurfBorder,velSurfBorder,velSurfSize[0]-velSurfBorder,velSurfSize[1]-2*velSurfBorder))

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

    def _updateZoom(self, zoom):
        """
        Creates and returns a surface containing the current zoom level.
        
        :param float zoom: The current zoom level.
        """

        zoomSurfSize = (215,40)
        zoomSurfBorder = 5
        zoomSurf = pg.Surface(zoomSurfSize)
        zoomSurf.fill(self._hudBackgroundColor)
        zoomSurf.fill(self._hudForegroundColor, (zoomSurfBorder,zoomSurfBorder,zoomSurfSize[0]-zoomSurfBorder,zoomSurfSize[1]-2*zoomSurfBorder))

        zoomString = "Zoom: "

        zoomMag = int(math.log2(zoom))

        zoomNumber = 2**abs(zoomMag)

        # find the number of spaces we need to pad the string with
        zoomString += " " * min(12, int(11-math.log10(zoomNumber))) if zoomMag < 0 else " " * min(12, int(13-math.log10(zoomNumber)))
        zoomString += "1/" + str(zoomNumber) if zoomMag < 0 else str(zoomNumber)
        zoomString += "x"

        textSize = self._bigFont.size(zoomString)
        zoomTextPosition = ((zoomSurf.get_height()-textSize[1])/2 + textSize[0]/2, zoomSurf.get_height()/2)
        graph.drawTextCenter(zoomTextPosition, zoomString, self._bigFont, self._fontColor, zoomSurf)

        return zoomSurf

    def _updateTimeScale(self, scale):
        """
        Creates and returns a surface containing the current ammount time is scaled by.
        
        :param float scale: The current ammount time is scaled by.
        """
        scaleSurfSize = (215,40)
        scaleSurfBorder = 5
        scaleSurf = pg.Surface(scaleSurfSize)
        scaleSurf.fill(self._hudBackgroundColor)
        scaleSurf.fill(self._hudForegroundColor, (scaleSurfBorder,scaleSurfBorder,scaleSurfSize[0]-scaleSurfBorder,scaleSurfSize[1]-2*scaleSurfBorder))

        scaleString = "Time Scale: "

        scaleMag = int(math.log2(scale))

        scaleNumber = 2**abs(scaleMag)

        # find the number of spaces we need to pad the string with
        scaleString += " " * min(6, int(5-math.log10(scaleNumber))) if scaleMag < 0 else " " * min(6, int(7-math.log10(scaleNumber)))
        scaleString += "1/" + str(scaleNumber) if scaleMag < 0 else str(scaleNumber)
        scaleString += "x"

        textSize = self._bigFont.size(scaleString)
        scaleTextPosition = ((scaleSurf.get_height()-textSize[1])/2 + textSize[0]/2, scaleSurf.get_height()/2)
        graph.drawTextCenter(scaleTextPosition, scaleString, self._bigFont, self._fontColor, scaleSurf)

        return scaleSurf

    def _updateSASFuel(self, rocket):
        """
        Creates and returns a surface containing the ammound of SAS Fuel that the provided
        rocket has remaining.
        
        :param rockets.rocket rocket: The rocket who's SAS Fuel should be displayed.
        """

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
        """
        Creates and returns a surface displaying the ammount of fuel left in each of the thrusters on the provided rocket
        
        :param rockets.rocket rocket: The rocket who's thruster fuel should be displayed.
        """

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
        """
        Creates and returns a surface indicating whether or not the provided rocket is currently locked to an angle using SAS.
        
        :param rockets.rocket rocket: The rocket who's SAS state should be checked.
        """

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
        Draws relevant information from the provided rocket to the screen, like the throttle,
        velocity, and fuel. Also displays time and zoom information.
        """
        
        navBallPos = (int(pg.display.get_surface().get_width()/2 - self._navBallRadius), int(pg.display.get_surface().get_height()-2*self._navBallRadius))
        pg.display.get_surface().blit(self._updateNavBall(rocket), navBallPos)

        throttleGauge = self._updateThrottle(rocket)
        throttlePos = (navBallPos[0] - throttleGauge.get_width(), navBallPos[1])
        pg.display.get_surface().blit(self._updateThrottle(rocket), throttlePos)

        velocity = self._updateVelocity(rocket)
        velocityPos = (throttlePos[0]-velocity.get_width(), pg.display.get_surface().get_height()-velocity.get_height())
        pg.display.get_surface().blit(self._updateVelocity(rocket), velocityPos)

        zoom = self._updateZoom(Drawer.zoom.zoom)
        zoomPos = (velocityPos[0], velocityPos[1]-zoom.get_height())
        pg.display.get_surface().blit(zoom, zoomPos)

        timeScale = self._updateTimeScale(TimeScale.scale)
        timeScalePos = (zoomPos[0], zoomPos[1]-timeScale.get_height())
        pg.display.get_surface().blit(timeScale, timeScalePos)

        sasFuel = self._updateSASFuel(rocket)
        sasFuelPos = (navBallPos[0] + 2*self._navBallRadius, navBallPos[1])
        pg.display.get_surface().blit(sasFuel, sasFuelPos)

        sasIndicator = self._updateSASIndicator(rocket)
        sasIndicatorPos = (sasFuelPos[0] + sasFuel.get_width(), pg.display.get_surface().get_height() - sasIndicator.get_height())
        pg.display.get_surface().blit(sasIndicator, sasIndicatorPos)

        thrusterFuel = self._updateThrusterFuel(rocket)
        thrusterFuelPos = (pg.display.get_surface().get_width() - thrusterFuel.get_width(), pg.display.get_surface().get_height() - thrusterFuel.get_height())
        pg.display.get_surface().blit(thrusterFuel, thrusterFuelPos)

