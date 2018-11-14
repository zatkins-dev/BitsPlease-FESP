import pygame as py
import pygame.gfxdraw as pygf
from physics import Physics as phy

class TrajectoryCalc():

    def __init__(self):
        self._xPosition = []
        self._yPosition = []
        self._xVelocity = 0
        self._yVelocity = 0
        self._vDeg = 0
        self._xAccel = []
        self._yAccel = []
        self._aDeg = 0
        self._points = []
        #self._xControl = 0
        #self._yControl = 0
        #self._xFinal = 0
        #self._yFinal = 0
        self._time = 0

    def updateTrajectory(self, surface, x, y, Vx, Vy, Vdeg, Ax, Ay, Adeg, time, celestialBodies, offset=0):
        self._xPosition = []
        self._yPosition = []
        self._xVelocity = 0
        self._yVelocity = 0
        self._vDeg = 0
        self._xAccel = []
        self._yAccel = []
        self._aDeg = 0
        self._points = []
        #self._xControl = 0
        #self._yControl = 0
        #self._xFinal = 0
        #self._yFinal = 0
        self._time = 0
        self._xPosition.append(x)
        self._yPosition.append(y)
        self._xVelocity = Vx
        self._yVelocity = Vy
        self._vDeg = Vdeg
        self._xAccel.append(Ax)
        self._yAccel.append(Ay)
        self._aDeg = Adeg
        self._time = time

        #self._xFinal = self._xPosition + self._xVelocity * self._time + .5 * self._xAccel * self._time**2
        #self._yFinal = self._yPosition + self._yVelocity * self._time + .5 * self._yAccel * self._time**2

        #self._xControl = (-self._xVelocity)/(2*self._xAccel)*(self._time) + self._xPosition
        #self._yControl = (-self._yVelocity)/(2*self._yAccel)*(self._time) + self._yPosition
        #print([self._xPosition, self._yPosition])

        #self._xPosition = self._xPosition + offset[0]
        #self._yPosition = self._yPosition + offset[1]
        #self._xControl = self._xControl + offset[0]
        #self._yControl = self._yControl + offset[1]
        #self._xFinal = self._xFinal + offset[0]
        #self._yFinal = self._yFinal + offset[1]

        #print([self._xPosition, self._yPosition])
        #self._points.append([self._xPosition, self._yPosition])
        #for i in range(time):
        #    point = [self._points[i-1][0] + self._xVelocity * self._time + .5 * self._xAccel * self._time**2, self._points[i-1][1] + self._yVelocity * self._time + .5 * self._yAccel * self._time**2]
        #    self._points.append(point)
        #py.draw.lines(surface, (255,255,255), False, self._points)

        #for each i in time, calculate the trajectory and draw the line
        #self._points.append([self._xPosition[1] + offset[1], self._yPosition[1] + offset[1]])

        for i in range(time):
            if(i == 0):
                self._points.append((x + offset[0], y + offset[1]))
                continue
            #calculate x, y position for each i
            grav = phy.netGravity(celestialBodies, [self._xPosition[i-1], self._yPosition[i-1]])

            self._xAccel.append(grav[0])
            self._yAccel.append(grav[1])
            self._xPosition.append(self._xPosition[i-1] + self._xVelocity * 1 + .5 * self._xAccel[i-1] * 1**2)
            self._yPosition.append(self._yPosition[i-1] - self._yVelocity * 1 - .5 * self._yAccel[i-1] * 1**2)
            self._points.append((self._xPosition[i] + offset[0], self._yPosition[i] + offset[1]))

        py.draw.aalines(surface, (255,255,255), False, self._points)
        #pygf.bezier(surface, [(self._xPosition, self._yPosition),(self._xControl, self._yControl),(self._xFinal, self._yFinal)], self._step, (255, 255, 255))
