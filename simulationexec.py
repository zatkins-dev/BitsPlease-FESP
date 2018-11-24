import pygame as pg
import pymunk as pm
from pymunk.vec2d import Vec2d
import sys
import os
import rockets.testrocket as tr
import math
from physics import *
from rockets import Thruster
from functools import reduce

from graphics import HUD
from graphics import Graphics as graph
from graphics import Drawer
from graphics import Trajectory
from graphics import Explosion
from graphics import Menu

from audio import AudioManager

import pymunkoptions
pymunkoptions.options["debug"] = False

ASSETS_PATH = os.path.abspath("assets/")

def keyDown(e, key):
    return e.type == pg.KEYDOWN and e.key == key


def keyUp(e, key):
    return e.type == pg.KEYUP and e.key == key


def updateGravity(space, rocket, objects):
    # space.gravity = Physics.netGravity(objects, rocket)
    deltaV = Vec2d(Physics.netGravity(objects, rocket.position))
    pm.Body.update_velocity(rocket, deltaV, 1, TimeScale.step_size)
    return deltaV


def updateCamera(screen, center):
    screen.fill((0, 0, 0))
    graph.drawStars(screen, center)


def get_altitude(celestialBodies, rocket):
    closestBody = min(celestialBodies, key=lambda x: (x.body.position - rocket.position).get_length())
    altitude = (closestBody.body.position - rocket.position).get_length() - closestBody.radius
    return (closestBody, altitude)


def clear(space):
    for s in space.shapes:
        space.remove(s)
    for b in space.bodies:
        space.remove(b)
    space.step(TimeScale.step_size)

def displayMenu(space):
    Menu.drawMenu(100)
    pg.display.flip()
    if Menu.quitPressed:
        Menu.quitPressed = False
        clear(space)
        return Menu.State.Exit
    elif Menu.demoPressed:
        Menu.demoPressed = False
        clear(space)
        return Menu.State.Playing
    elif Menu.builderPressed:
        Menu.builderPressed = False
        clear(space)
        return Menu.State.Building
    else:
        return None


def run(rocket=None):
    sasActive = False #For use in AudioManager
    audioManager = AudioManager()
    celestialBodies = []
    screen = pg.display.get_surface()
    clock = pg.time.Clock()
    explosion_images = []
    for i in range(5):
            explosion_images.append(pg.image.load(os.path.join(ASSETS_PATH,"sprites/explosion"+str(i+1)+".png")).convert_alpha())
    space = pm.Space(threaded=True)
    space.threads = 2
    hud = HUD()

    earth = CelestialBody('earth', space, 9.331*10**22, 796375, 0, 0, 0.99999, (128,200,255), 100000, pm.Body.DYNAMIC)
    celestialBodies.append(earth)

    earthMoon1 = CelestialBody('earthMoon1', space, 1.148*10**21, 217125,
                    796375 + 43500000, 796375, 0.9, None, 0, pm.Body.DYNAMIC)
    celestialBodies.append(earthMoon1)

    if rocket is None:
        rocket = tr.genRocket(space)
    else:
        space.add(rocket)
        for component in rocket.components:
            space.add(component)

    space.damping = 1

    x, y = (0, earth.posy + earth.radius)
    rocket.position = int(x), int(y)

    # Add collision handler
    collisions_component_celestialbody = space.add_collision_handler(CT_COMPONENT, CT_CELESTIAL_BODY)
    collisions_component_celestialbody.post_solve = post_solve_component_celestialbody

    rocket_explosion = None
    crashed = False
    menu_enabled = False
    Menu.demoPressed = False
    Menu.builderPressed = False
    while not crashed:
        audioManager.musicChecker()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return Menu.State.Exit
            elif keyDown(event, pg.K_ESCAPE):
                menu_enabled = True
                Menu.demoPressed = False
            elif keyUp(event, pg.K_ESCAPE):
                menu_enabled = False
            elif keyDown(event, pg.K_MINUS):
                TimeScale.slower()
            elif keyDown(event, pg.K_EQUALS):
                TimeScale.faster()
            elif event.type == pg.KEYDOWN:
                rocket.handleEvent(event)

            elif event.type == pg.VIDEORESIZE:
                screen = pg.display.set_mode((event.w, event.h), pg.RESIZABLE)

            elif event.type == pg.MOUSEBUTTONDOWN and menu_enabled == False:
                if event.button == 4:
                    Drawer.zoom.zoom_out()
                elif event.button == 5:
                    Drawer.zoom.zoom_in()
        rocket.tick(TimeScale.scale)
        audioManager.thrusterSoundEffect(rocket.throttle)
        audioManager.sasSoundEffect(rocket.isAngleLocked)

        grav = updateGravity(space, rocket, celestialBodies)

        pos = rocket.position
        vel = rocket.velocity
        (closestBody, altitude) = get_altitude(celestialBodies, rocket)

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
        if altitude < vel.length*TimeScale.scale*64:
            Drawer.zoom.reset()

        space.step(TimeScale.step_size)

        offset = Drawer.getOffset(screen, rocket)

        updateCamera(screen, offset)
        Drawer.drawBackground(closestBody, altitude)
        Trajectory.draw(rocket, celestialBodies, 1000, 1)
        Drawer.drawMultiple(screen, space.shapes, offset)
        Drawer.drawMultiple(screen, celestialBodies, offset)
        hud.updateHUD(rocket)
        # Did the rocket blow up?
        if rocket.destroyed and rocket_explosion is None:
            for c in rocket.components:
                c.destroyed = True
            remaining_fuel = sum(map(lambda c: c.fuel if isinstance(c, Thruster) else 0, rocket.components))
            rocket_explosion = Explosion(remaining_fuel//10, explosion_images)
            rocket.velocity = grav
            crashed = True

        if menu_enabled:
            returnCode = displayMenu(space)
            if returnCode is not None:
                TimeScale.reset()
                Drawer.zoom.reset()
                return returnCode
        pg.display.flip()
        clock.tick(60)

    Menu.demoPressed = False
    TimeScale.reset()
    Drawer.zoom.reset()
    displayMenu(space)
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT or keyDown(event, pg.K_ESCAPE):
                return Menu.State.Exit
        space.step(TimeScale.step_size)
        rocket.velocity = (0,0)
        offset = Drawer.getOffset(screen, rocket)
        updateCamera(screen, offset)
        Drawer.drawMultiple(screen, space.shapes, offset)
        Drawer.drawMultiple(screen, celestialBodies, offset)
        Drawer.drawExplosion(screen, rocket_explosion, rocket.position + 20*Vec2d(0,1).rotated(rocket.angle), (150,150), Drawer.getOffset(screen, rocket))
        returnCode = displayMenu(space)
        if returnCode is not None:
            return returnCode
        pg.display.flip()
        clock.tick(60)



if __name__ == "__main__":
    run()
