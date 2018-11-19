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
from graphics import TrajectoryCalc
from graphics import Explosion
from graphics import Menu

import pymunkoptions
pymunkoptions.options["debug"] = False

res_x, res_y = 1000, 1000
GROUND_Y = res_y/20
G = 6.67408*10**-11
ASSETS_PATH = os.path.abspath("assets/")

def keyDown(e, key):
    return e.type == pg.KEYDOWN and e.key == key


def keyUp(e, key):
    return e.type == pg.KEYUP and e.key == key


def updateGravity(space, rocket, objects, ticksPerSec):
    # space.gravity = Physics.netGravity(objects, rocket)
    deltaV = Vec2d(Physics.netGravity(objects, rocket.position))
    pm.Body.update_velocity(rocket, deltaV, 1, 1/ticksPerSec)
    return deltaV


def updateCamera(screen, center):
    screen.fill((0, 0, 0))
    graph.drawStars(screen, center)

def clear(space):
    for s in space.shapes:
        space.remove(s)
    for b in space.bodies:
        space.remove(b)
    space.step(1/50)

def displayMenu(space):
    Menu.drawMenu(100)
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

def run():
    pg.mixer.init()
    pg.mixer.music.load("sound/Sci-fiPulseLoop.wav")
    celestialBodies = []
    screen = pg.display.get_surface()
    clock = pg.time.Clock()
    explosion_images = []
    for i in range(5):
            explosion_images.append(pg.image.load(os.path.join(ASSETS_PATH,"sprites/explosion"+str(i+1)+".png")).convert_alpha())
    space = pm.Space(threaded=True)
    space.threads = 2
    hud = HUD()
    traj = TrajectoryCalc()

    earth = CelestialBody('earth', space, 9.331*10**22, 796375, 0, 0, 0.99999, 0, pm.Body.DYNAMIC)
    celestialBodies.append(earth)

    earthMoon1 = CelestialBody('earthMoon1', space, 1.148*10**21, 217125,
                    796375 + 43500000, 796375, 0.9, 0, pm.Body.DYNAMIC)
    celestialBodies.append(earthMoon1)

    # planetGage = CelestialBody('planetGage', space, 10**12, 200, 1000, 1000, 0.9, 0, 0)
    # celestialBodies.append(planetGage)
    #
    # planetThomas = CelestialBody('planetThomas', space, 10**13, 200, 1500, 1500, .9, 0, 0)
    # celestialBodies.append(planetThomas)
    #
    # planetZach = CelestialBody('planetZach', space, 10**13, 200, 2000, 1000, 0.9, 0, 0)
    # celestialBodies.append(planetZach)

    rocket = tr.genRocket(space)
    rocket.debugComponentPrint()
    # draw_options = pygame_util.DrawOptions(game)
    space.damping = 1

    x, y = (0, earth.posy + earth.radius)
    rocket.position = int(x), int(y)
    print (rocket.position)
    ticksPerSec = 50.0
    pg.mixer.music.play(-1)

    # Add collision handler
    collisions_component_celestialbody = space.add_collision_handler(CT_COMPONENT, CT_CELESTIAL_BODY)
    collisions_component_celestialbody.post_solve = post_solve_component_celestialbody
    keyInputs = []
    rocket_explosion = None
    crashed = False
    menu_enabled = False
    while not crashed:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return Menu.State.Exit
            elif keyDown(event, pg.K_ESCAPE):
                menu_enabled = True
                Menu.demoPressed = False
            elif keyUp(event, pg.K_ESCAPE):
                menu_enabled = False
            elif event.type == pg.KEYDOWN:
                if not (event.key in keyInputs):
                    keyInputs.append(event.key)

            elif event.type == pg.KEYUP:
                keyInputs.remove(event.key)


            elif event.type == pg.VIDEORESIZE:
                screen = pg.display.set_mode((event.w, event.h), pg.RESIZABLE)

            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 4:
                    if Drawer._zoom > Drawer._minZoom:
                        Drawer._zoom /= 2
                elif event.button == 5:
                    if Drawer._zoom < Drawer._maxZoom:
                        Drawer._zoom *= 2
                print("Zoom: {0}\n".format(Drawer._zoom))
                
        if keyInputs != [] :
            for i in keyInputs:
                rocket.handleEvent(i)

        grav = updateGravity(space, rocket, celestialBodies, ticksPerSec)
        space.step(1/ticksPerSec)
        pos = rocket.position
        vel = rocket.velocity
        offset = Drawer.getOffset(screen, rocket)

        updateCamera(screen, offset)
        # activeComponents = list(filter(lambda c: not c.destroyed, rocket.components))
        # destroyedComponents = list(filter(lambda c: c.destroyed, rocket.components))
        # for c in destroyedComponents:
        #     if c.sprite is not None:
        #         Drawer.drawExplosion(screen, c.cache_bb().center(), c.sprite.get_size(), Drawer.getOffset(screen, rocket))
        # updateTrajectory2(self, surface, position, velocity, timesteps, dt, planetBodies, rocket, offset)
        thrusters = filter(lambda c: isinstance(c, Thruster), rocket.components)
        totalThrust = sum(map(lambda t: t._thrustForce*t._thrustVector, thrusters))
        traj.updateTrajectory2(screen, pos, vel, 10, 0.5, totalThrust, celestialBodies, rocket, offset)
        Drawer.drawMultiple(screen, space.shapes, offset)
        Drawer.drawMultiple(screen, celestialBodies, offset)
        hud.updateHUD(pos[0], pos[1], (math.degrees(rocket.angle)+90) % 360,
                      vel.length, vel.angle_degrees % 360,
                      grav.length, grav.angle_degrees % 360,
                      rocket.components, clock.get_fps())
        # Did the rocket blow up?
        if rocket.destroyed and rocket_explosion is None:
            for c in rocket.components:
                c.destroyed = True
            remaining_fuel = sum(map(lambda c: c.fuel if isinstance(c, Thruster) else 0, rocket.components))
            rocket_explosion = Explosion(remaining_fuel//10, explosion_images)
            rocket.velocity = grav
            crashed = True
            # while rocket_explosion.duration>0:
            #     print(rocket_explosion.duration)
            #     Drawer.drawExplosion(screen, rocket_explosion, rocket.position + 20*Vec2d(0,1).rotated(rocket.angle), (150,150), Drawer.getOffset(screen, rocket))
            #     pg.display.flip()
            #     clock.tick(60)
        if menu_enabled:
            displayMenu(space)
        pg.display.flip()
        clock.tick(60)
    
    Menu.demoPressed = False
    displayMenu(space)
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT or keyDown(event, pg.K_ESCAPE):
                return Menu.State.Exit
        space.step(1/ticksPerSec)
        print("stepped")
        offset = Drawer.getOffset(screen, rocket)
        updateCamera(screen, offset)
        Drawer.drawMultiple(screen, space.shapes, offset)
        Drawer.drawMultiple(screen, celestialBodies, offset)
        Drawer.drawExplosion(screen, rocket_explosion, rocket.position + 20*Vec2d(0,1).rotated(rocket.angle), (150,150), Drawer.getOffset(screen, rocket))
        displayMenu(space)
        pg.display.flip()
        clock.tick(60)



if __name__ == "__main__":
    run()
