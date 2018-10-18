#This file will manage the display of mission critical information

import pygame as pg
from Graphics.Graphics import Graphics as graph
from Rockets.component import Component
from Rockets.thruster import Thruster
from Rockets.SAS import SAS
import math

class headsUpDisplay():

    def __init__(self):
        #pg.font.init()
        self._xPosition = 0
        self._yPosition = 0
        self._positionDegree = 0
        self._velocityMag = 0
        self._velocityDegree = 0
        self._accelerationMag = 0
        self._accelerationDegree = 0
        self._text = None
        self._thrusters = None
        self._SASmodules = None
        #self._pgFont = pg.font.SysFont("Times New Roman", 18)
        #self._textSurface = None

    def updateHUD(self, x, y, pDeg, vMag, vDeg, aMag, aDeg, components, fps):
        self._xPosition = x
        self._yPosition = y
        self._positionDegree = pDeg
        self._velocityMag = vMag
        self._velocityDegree = vDeg
        self._accelerationMag = aMag
        self._accelerationDegree = aDeg
        self.thrusters = filter(lambda c: isinstance(c, Thruster), components)
        self.SASmodules = filter(lambda c: isinstance(c, SAS), components)

        graph.drawText((150,10), "X Position: " + str("{:10.4f}".format(self._xPosition)) + " m", 20, (255,0,0), "Futura")
        graph.drawText((150,30), "Y Position: " + str("{:10.4f}".format(self._yPosition)) + " m", 20, (255,0,0), "Futura")
        graph.drawText((192,50), "Nose Degree: " + str("{:10.4f}".format(self._positionDegree)) + " degrees", 20, (255,0,0), "Futura")
        graph.drawText((210,70), "Velocity Magnitude: " + str("{:10.4f}".format(self._velocityMag)) + " m/s", 20, (255,0,0), "Futura")
        graph.drawText((217,90), "Velocity Degree: " + str("{:10.4f}".format(self._velocityDegree)) + " degrees", 20, (255,0,0), "Futura")
        graph.drawText((247,110), "Acceleration Magnitude: " + str("{:10.4f}".format(self._accelerationMag)) + " m/s^2", 20, (255,0,0), "Futura")
        graph.drawText((241,130), "Acceleration Degree: " + str("{:10.4f}".format(self._accelerationDegree)) + " degrees", 20, (255,0,0), "Futura")

        numThruster = 0
        for thruster in self.thrusters:
            numThruster = numThruster + 1
            graph.drawText((312,130 + numThruster*20), "Thruster Module " + str(numThruster) + " Fuel Remaining: " + str("{:10.0f}".format(thruster.fuel)) + " Liters", 20, (255,0,0), "Futura")

        numSAS = 0
        for sas in self.SASmodules:
            numSAS = numSAS + 1
            graph.drawText((282,130 + numThruster*20 + numSAS*20), "SAS Module " + str(numSAS) + " Fuel Remaining: " + str("{:10.0f}".format(sas.fuel)) + " Liters", 20, (255,0,0), "Futura")

        graph.drawText((70,150 + numThruster * 20 + numSAS * 20), "FPS: " + "{:0.3f}".format(fps), 20, (255,0,0), "Futura")