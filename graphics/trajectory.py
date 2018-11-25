import pygame as pg
from physics import Physics as phy
import math
from graphics import Drawer
from pymunk.vec2d import Vec2d


class Trajectory():
    """
    Drawer for the projected trajectory of the rocket.
    """

    @classmethod
    def hitsPlanet(cls, position, planets):
        """
        Helper function that provides a stopping condition 

        :param (float,float) position: Position to check
        :param planets: List of planets
        :type planets: [:py:class:`...physics.CelestialBody`]
        :returns: `True` if position is inside one of `planets`, `False` otherwise
        """

        for planet in planets:
            if planet.shape.point_query(position)[0] < 0:
                return True
        return False
    
    @classmethod
    def eulers(cls,f_prev,dt,dfdt):
        """
        Uses the forward Euler method to approximate the the value of a function at the next timestep. Specifically, returns :math:`f_{next} = f_{prev} + \Delta t\cdot\\frac{fp}{dt}`, where :math:`\\frac{df}{dt}` is the derivative of the fuction at the previous timestep.

        :param f_prev: Function value at previous timestep
        :type f_prev: :py:class:`pymunk.vec2d.Vec2d`
        :param float dt: Small change in time (:math:`\Delta t`), a smaller value yields a more accurate approximation
        :param dfdt: Value of the derivative :math:`\\frac{df}{dt}`.
        :type dfdt: :py:class:`pymunk.vec2d.Vec2d`
        :returns: Projected function value at the next timestep
        :rtype: :py:class:`pymunk.vec2d.Vec2d`
        """
        return Vec2d(f_prev + dt*Vec2d(dfdt))

    @classmethod
    def draw(cls, rocket, planetBodies, max_timesteps, dt):
        """
        Draws the projected path of the rocket until a stopping condition is reached, namely:
            * A point in the projection goes off the current display.
            * A point in the planet intersect a planetary body.
            * The iteration count exceeds `max_timesteps`.
        
        :param rocket: The rocket to project
        :type rocket: :py:class:`rockets.Rocket`
        :param planetBodies: List of all planetary bodies
        :type planetBodies: [:py:class:`physics.CelestialBody`]
        :param int max_timesteps: Maximum iterations before stopping
        :param float dt: Iteration step size
        """
        surface = pg.display.get_surface()
        offset = Drawer.getOffset(surface, rocket)
        x,y = surface.get_size()
        points = []
        
        dt = math.log(rocket.velocity.length+1.01)
        if Drawer.zoom.zoom < 1:
            dt = min(dt*-math.log2(Drawer.zoom.zoom), 10)
        elif Drawer.zoom.zoom > 1:
            dt = max(dt/math.log2(Drawer.zoom.zoom), 0.01)
        if dt == 0:
            return
        
        v_prev = rocket.velocity
        pos_prev = rocket.position
        points.append(pos_prev)
        curr_step = 0
        while Drawer.inRange((x,y), Drawer.zoom.zoom*(pos_prev+offset)) and curr_step < max_timesteps and not cls.hitsPlanet(pos_prev, planetBodies):
            if len(points)>40 and (pos_prev-points[0]).length < 1000:
                break
            v_prev = cls.eulers(v_prev, dt, phy.netGravity(planetBodies, pos_prev))
            pos_prev = cls.eulers(pos_prev, dt, v_prev)
            points.append(pos_prev)
            curr_step += 1
        
        points = list(map(lambda x: (x+offset)*Drawer.zoom.zoom, points))
        points = list(map(lambda x: (x[0],y-x[1]), points))

        if len(points) > 1:
            pg.draw.aalines(surface, (255,255,255), False, points)
            pg.draw.lines(surface, (255,255,255), False, list(map(Drawer.intVec2d, points)), 2)
