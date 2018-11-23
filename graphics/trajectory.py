import pygame as pg
from physics import Physics as phy
import math
from graphics import Drawer
from pymunk.vec2d import Vec2d


class Trajectory():
    @classmethod
    def hitsPlanet(cls, position, planets):
        for planet in planets:
            if planet.shape.point_query(position)[0] < 0:
                return True
        return False
    
    @classmethod
    def velocity(cls,v_prev,dt,mass,grav,k):
        dvdt = grav - k/mass * Vec2d(v_prev[0]**2, v_prev[1]**2)
        return Vec2d(v_prev + dt*dvdt)
    
    @classmethod
    def position(cls,pos_prev,dt,velocity):
        return Vec2d(pos_prev + dt*velocity)

    @classmethod
    def draw(cls, surface, position, velocity, timesteps, dt, planetBodies, rocket, offset):
        x,y = surface.get_size()
        points = []
        points.append(position)
        dt = math.log(velocity.length+1.01)
        if Drawer.zoom.zoom < 1:
            dt = min(dt*-math.log2(Drawer.zoom.zoom), 10)
        elif Drawer.zoom.zoom > 1:
            dt = max(dt/math.log2(Drawer.zoom.zoom), 0.01)
        if dt == 0:
            return
        v_prev = velocity
        pos_prev = position
        curr_step = 0
        while Drawer.inRange((x,y), Drawer.zoom.zoom*(pos_prev+offset)) and curr_step < timesteps and not cls.hitsPlanet(pos_prev, planetBodies):
            if len(points)>40 and (pos_prev-points[0]).length < 1000:
                break
            v_prev = cls.velocity(v_prev,dt,rocket.mass,phy.netGravity(planetBodies, pos_prev), 0)
            pos_prev = cls.position(pos_prev, dt, v_prev)
            points.append(pos_prev)
            curr_step += 1
        
        points = list(map(lambda x: (x+offset)*Drawer.zoom.zoom, points))
        points = list(map(lambda x: (x[0],y-x[1]), points))

        if len(points) > 1:
            pg.draw.aalines(surface, (255,255,255), False, points)
            pg.draw.lines(surface, (255,255,255), False, list(map(Drawer.intVec2d, points)), 2)
