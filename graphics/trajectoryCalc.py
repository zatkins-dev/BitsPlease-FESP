import pygame as pg
import pygame.gfxdraw as pygf
from physics import Physics as phy
import math
from graphics import Drawer
from pymunk.vec2d import Vec2d


class TrajectoryCalc():
    def __init__(self):
        self._xPosition = []
        self._yPosition = []
        self._xVelocity = []
        self._yVelocity = []
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
        self._dt = 0.5
        # self._pixelArr = pg.PixelArray(pg.Surface(pg.display.get_surface().get_size()))
    def hitsPlanet(self, position, planets):
        for planet in planets:
            if planet.shape.point_query(position)[0] < 0:
                return True
        return False
    def velocity(self,v_prev,dt,mass,grav,k):
        dvdt = grav - k/mass * Vec2d(v_prev[0]**2, v_prev[1]**2)
        return Vec2d(v_prev + dt*dvdt)
    def position(self,pos_prev,dt,velocity):
        return Vec2d(pos_prev + dt*velocity)
    def updateTrajectory2(self, surface, position, velocity, timesteps, dt, planetBodies, rocket, offset):
        x,y = surface.get_size()
        self._points = []
        self._points.append(position)
        dt = math.log(velocity.length+1.01)
        if Drawer._zoom < 1:
            dt = min(dt*-math.log2(Drawer._zoom), 10)
        elif Drawer._zoom > 1:
            dt = max(dt/math.log2(Drawer._zoom), 0.01)
        if dt == 0:
            return
        v_prev = velocity
        pos_prev = position
        curr_step = 0
        while Drawer.inRange((x,y), Drawer._zoom*(pos_prev+offset)) and curr_step < timesteps and not self.hitsPlanet(pos_prev, planetBodies):
            if len(self._points)>40 and (pos_prev-self._points[0]).length < 1000:
                break
            v_prev = self.velocity(v_prev,dt,rocket.mass,phy.netGravity(planetBodies, pos_prev), 0)
            pos_prev = self.position(pos_prev, dt, v_prev)
            self._points.append(pos_prev)
            curr_step += 1
        
        self._points = list(map(lambda x: (x+offset)*Drawer._zoom, self._points))
        self._points = list(map(lambda x: (x[0],y-x[1]), self._points))

        if len(self._points) > 1:
            pg.draw.aalines(surface, (255,255,255), False, self._points)
            pg.draw.lines(surface, (255,255,255), False, list(map(Drawer.intVec2d, self._points)), 2)
                

    def updateTrajectory(self, surface, x, y, Vx, Vy, Vdeg, Ax, Ay, Adeg, time, dt, celestialBodies, offset=0):
        self._xPosition = []
        self._yPosition = []
        self._xVelocity = []
        self._yVelocity = []
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
        self._xVelocity.append(Vx)
        self._yVelocity.append(Vy)
        self._vDeg = Vdeg
        self._xAccel.append(Ax)
        self._yAccel.append(Ay)
        self._aDeg = Adeg
        self._time = time
        testdt = self._dt
        if Drawer._zoom == 1:
            self._time = time
        elif Drawer._zoom > 1:
            self._time = math.ceil(time/math.log2(Drawer._zoom))
        else:
            self._time = 2*math.ceil(time*-math.log2(Drawer._zoom))

        for i in range(self._time):
            if(i == 0):
                point = Vec2d(x + offset[0], y + offset[1])*Drawer._zoom
                self._points.append(point)
                continue
            #calculate x, y position for each i
            grav = phy.netGravity(celestialBodies, [self._xPosition[i-1], self._yPosition[i-1]])

            self._xAccel.append(grav[0])
            self._yAccel.append(grav[1])
            self._xVelocity.append(self._xVelocity[i-1] + self._xAccel[i-1] * self._dt)
            self._yVelocity.append(self._yVelocity[i-1] - self._yAccel[i-1] * self._dt)
            self._xPosition.append(self._xPosition[i-1] + self._xVelocity[i-1] * self._dt + .5 * self._xAccel[i-1] * self._dt**2)
            self._yPosition.append(self._yPosition[i-1] - self._yVelocity[i-1] * self._dt - .5 * self._yAccel[i-1] * self._dt**2)
            self._points.append(Vec2d(self._xPosition[i] + offset[0], self._yPosition[i] + offset[1])*Drawer._zoom)
            
        pg.draw.aalines(surface, (255,255,255), False, self._points)
        pg.draw.lines(surface, (255,255,255), False, list(map(Drawer.intVec2d, self._points)), 2)
