import pygame as pg
import pymunk as pm
from pymunk.vec2d import Vec2d
import sys
import os
import math

from physics import *

from rockets import Thruster
import rockets.testrocket as tr

from functools import reduce

from graphics import HUD
from graphics import Graphics as graph
from graphics import Drawer
from graphics import Trajectory
from graphics import Explosion
from graphics import Menu
from graphics import Video
from graphics import Zoom

from audio import AudioManager


import pymunkoptions
pymunkoptions.options["debug"] = False

class Simulation():
    ASSETS_PATH = os.path.abspath("assets/")
    _zoom = Zoom()

    @classmethod
    def keyDown(cls, e, key):
        return e.type == pg.KEYDOWN and e.key == key

    @classmethod
    def keyUp(cls, e, key):
        return e.type == pg.KEYUP and e.key == key

    @classmethod
    def updateGravity(cls):
        deltaV = Vec2d(Physics.netGravity(cls.celestialBodies, cls.rocket.position))
        pm.Body.update_velocity(cls.rocket, deltaV, 1, TimeScale.step_size)
        return deltaV

    @classmethod
    def updateCamera(cls, center):
        cls.screen.fill((0, 0, 0))
        graph.drawStars(cls.screen, center)

    @classmethod
    def get_altitude(cls):
        closestBody = min(cls.celestialBodies, key=lambda x: (x.body.position - cls.rocket.position).get_length())
        altitude = (closestBody.body.position - cls.rocket.position).get_length() - closestBody.shape.radius
        return (closestBody, altitude)

    @classmethod
    def clear_space(cls):
        for s in cls.space.shapes:
            cls.space.remove(s)
        for b in cls.space.bodies:
            cls.space.remove(b)
        cls.space.step(TimeScale.step_size)

    @classmethod
    def displayMenu(cls):
        Menu.drawMenu(100)
        pg.display.flip()
        if Menu.quitPressed:
            Menu.quitPressed = False
            cls.clear_space()
            return Menu.State.Exit
        elif Menu.demoPressed:
            Menu.demoPressed = False
            cls.clear_space()
            return Menu.State.Playing
        elif Menu.builderPressed:
            Menu.builderPressed = False
            cls.clear_space()
            return Menu.State.Building
        else:
            return None


    @classmethod
    def run(cls,rocket=None):
        cls._zoom = Zoom()
        Drawer.zoom = cls._zoom
        cls.audioManager = AudioManager()
        cls.celestialBodies = []
        cls.screen = pg.display.get_surface()
        cls.clock = pg.time.Clock()
        explosion_images = []
        for i in range(5):
                explosion_images.append(pg.image.load(os.path.join(cls.ASSETS_PATH,"sprites/explosion"+str(i+1)+".png")).convert_alpha())
        cls.space = pm.Space(threaded=True)
        cls.space.threads = 2
        hud = HUD()

        earth = CelestialBody('earth', cls.space, 9.331*10**22, 796375, (0, 0), 0.99999, (128,200,255), 100000, pm.Body.DYNAMIC)
        cls.celestialBodies.append(earth)

        earthMoon1 = CelestialBody('earthMoon1', cls.space, 1.148*10**21, 217125,
                        (796375 + 43500000, 796375), 0.9, None, 0, pm.Body.DYNAMIC)
        cls.celestialBodies.append(earthMoon1)

        cls.rocket = rocket if rocket is not None else tr.genRocket(cls.space)
        if cls.rocket is rocket:
            cls.space.add(cls.rocket)
            for component in cls.rocket.components:
                cls.space.add(component)

        cls.space.damping = 1

        x, y = (0, earth.body.position[1] + earth.shape.radius)
        cls.rocket.position = int(x), int(y)

        # Add collision handler
        collisions_component_celestialbody = cls.space.add_collision_handler(CT_COMPONENT, CT_CELESTIAL_BODY)
        collisions_component_celestialbody.post_solve = post_solve_component_celestialbody

        cls.rocket_explosion = None
        crashed = False
        menu_enabled = False
        Menu.demoPressed = False
        Menu.builderPressed = False
        while not crashed:
            cls.audioManager.musicChecker()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return Menu.State.Exit
                elif cls.keyDown(event, pg.K_ESCAPE):
                    menu_enabled = True
                    Menu.demoPressed = False
                elif cls.keyUp(event, pg.K_ESCAPE):
                    menu_enabled = False
                elif cls.keyDown(event, pg.K_MINUS):
                    TimeScale.slower()
                elif cls.keyDown(event, pg.K_EQUALS):
                    TimeScale.faster()
                elif event.type == pg.KEYDOWN:
                    cls.rocket.handleEvent(event)

                elif event.type == pg.VIDEORESIZE:
                    Video.set_display(event.w, event.h)
                    cls.screen = Video.get_display()

                elif event.type == pg.MOUSEBUTTONDOWN and menu_enabled == False:
                    if event.button == 4:
                        Drawer.zoom.zoom_out()
                    elif event.button == 5:
                        Drawer.zoom.zoom_in()
            cls.rocket.tick(TimeScale.scale)
            cls.audioManager.thrusterSoundEffect(len(cls.rocket.thrusters) != 0, cls.rocket.throttle)
            cls.audioManager.sasSoundEffect(len(cls.rocket.SASmodules) != 0 and cls.rocket.isAngleLocked)

            grav = cls.updateGravity()

            (closestBody, altitude) = cls.get_altitude()
            if altitude < 500000:
                while TimeScale.scale > 256:
                    TimeScale.slower()
            if altitude < 50000:
                while TimeScale.scale > 32:
                    TimeScale.slower()
            if altitude < 25000:
                while TimeScale.scale > 4:
                    TimeScale.slower()
            if altitude < 12500:
                while TimeScale.scale > 2:
                    TimeScale.slower()

            if TimeScale.scale > 1 and cls.rocket.isAngleLocked:
                cls.rocket.isAngleLocked = False

            cls.space.step(TimeScale.step_size)

            cls.offset = Drawer.getOffset(cls.screen, cls.rocket)

            cls.updateCamera(Drawer.intVec2d(Vec2d(cls.screen.get_size())))
            Drawer.drawBackground(closestBody, altitude, cls.offset)
            Trajectory.draw(cls.rocket, cls.celestialBodies, 1000, 1)
            Drawer.drawMultiple(cls.screen, cls.space.shapes, cls.offset)
            Drawer.drawMultiple(cls.screen, cls.celestialBodies, cls.offset)
            hud.updateHUD(cls.rocket)
            # Did the cls.rocket blow up?
            if cls.rocket.destroyed and cls.rocket_explosion is None:
                for c in cls.rocket.components:
                    c.destroyed = True
                remaining_fuel = sum(map(lambda c: c.fuel if isinstance(c, Thruster) else 0, cls.rocket.components))
                cls.rocket_explosion = Explosion(remaining_fuel//10, explosion_images)
                cls.rocket.velocity = grav
                crashed = True

            if menu_enabled:
                returnCode = cls.displayMenu()
                if returnCode is not None:
                    TimeScale.reset()
                    Drawer.zoom.reset()
                    cls.audioManager.silenceMusic()
                    return returnCode
            pg.display.flip()
            cls.clock.tick(60)

        Menu.demoPressed = False
        TimeScale.reset()
        cls.displayMenu()
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT or cls.keyDown(event, pg.K_ESCAPE):
                    return Menu.State.Exit
            cls.space.step(TimeScale.step_size)
            cls.rocket.velocity = (0,0)
            (closestBody, altitude) = cls.get_altitude()

            cls.offset = Drawer.getOffset(cls.screen, cls.rocket)
            cls.updateCamera(Drawer.intVec2d(Vec2d(cls.screen.get_size())))
            Drawer.drawBackground(closestBody, altitude, cls.offset)
            Drawer.drawMultiple(cls.screen, cls.space.shapes, cls.offset)
            Drawer.drawMultiple(cls.screen, cls.celestialBodies, cls.offset)
            Drawer.drawExplosion(cls.screen, cls.rocket_explosion, cls.rocket.position + 20*Vec2d(0,1).rotated(cls.rocket.angle), (150,150), Drawer.getOffset(cls.screen, cls.rocket))
            returnCode = cls.displayMenu()
            if returnCode is not None:
                return returnCode
            pg.display.flip()
            cls.clock.tick(60)
