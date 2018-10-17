#This file will manage the display of mission critical information

import pygame as pg
from Graphics.Graphics import Graphics as graph
import math

class headsUpDisplay():

    def __init__(self):
        #pg.font.init()
        self._xPosition = 0
        self._yPosition = 0
        self._velocityMag = 0
        self._velocityDegree = 0
        self._accelerationMag = 0
        self._accelerationDegree = 0
        self._text = None
        #self._pgFont = pg.font.SysFont("Times New Roman", 18)
        #self._textSurface = None

    def updateHUD(self, x, y, vMag, vDeg, aMag, aDeg):
        self._xPosition = x
        self._yPosition = y
        self._velocityMag = vMag
        self._velocityDegree = vDeg
        self._accelerationMag = aMag
        self._accelerationDegree = aDeg
        self._text = "X Position: " + str("{:10.4f}".format(self._xPosition)) + " meters"

        graph.drawText((150,10), "X Position: " + str("{:10.4f}".format(self._xPosition)) + " m", 20, (255,0,0), "Times New Roman")
        graph.drawText((150,30), "Y Position: " + str("{:10.4f}".format(self._yPosition)) + " m", 20, (255,0,0), "Times New Roman")
        graph.drawText((210,50), "Velocity Magnitude: " + str("{:10.4f}".format(self._velocityMag)) + " m/s", 20, (255,0,0), "Times New Roman")
        graph.drawText((217,70), "Velocity Degree: " + str("{:10.4f}".format(self._velocityDegree)) + " degrees", 20, (255,0,0), "Times New Roman")
        graph.drawText((247,90), "Acceleration Magnitude: " + str("{:10.4f}".format(self._accelerationMag)) + " m/s^2", 20, (255,0,0), "Times New Roman")
        graph.drawText((241,110), "Acceleration Degree: " + str("{:10.4f}".format(self._accelerationDegree)) + " degrees", 20, (255,0,0), "Times New Roman")
