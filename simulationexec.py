import pygame as pg
import pymunk as pm
from pymunk.vec2d import Vec2d
import sys
import os
import rockets.testrocket as tr
import math
from physics import * 

from graphics import HUD
from graphics import Graphics as graph
from graphics import Drawer

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
    deltaV = Vec2d(Physics.netGravity(objects, rocket))
    pm.Body.update_velocity(rocket, deltaV, 1, 1/ticksPerSec)
    return deltaV


def updateCamera(screen, center):
    screen.fill((0, 0, 0))
    graph.drawStars(screen, center)


def run():
    pg.mixer.init()
    pg.mixer.music.load("sound/Sci-fiPulseLoop.wav")
    celestialBodies = []
    screen = pg.display.get_surface()
    clock = pg.time.Clock()

    space = pm.Space(threaded=True)
    space.threads = 2
    hud = HUD()

    earth = CelestialBody('earth', space, 9.331*10**22, 796375, 0, 0, 0.9, 0, pm.Body.DYNAMIC)
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

    # draw_options = pygame_util.DrawOptions(game)
    space.damping = 1

    fire = False
    rotate = False
    auto = False
    sas_angle = 0

    x, y = (0, earth.posx + earth.radius)
    rocket.position = int(x), int(y)

    ticksPerSec = 50.0
    pg.mixer.music.play(-1)
    print(rocket.position)

    # Add collision handler
    collisions_component_celestialbody = space.add_collision_handler(CT_COMPONENT, CT_CELESTIAL_BODY)
    collisions_component_celestialbody.post_solve = post_solve_component_celestialbody
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT or keyDown(event, pg.K_ESCAPE):
                pg.quit()
                sys.exit(0)
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_a or event.key == pg.K_d:
                    rotKey = event.key
                    rotate = True
                elif event.key == pg.K_f:
                    fireKey = event.key
                    fire = True

            elif event.type == pg.KEYUP:
                if event.key == pg.K_a or event.key == pg.K_d:
                    rotate = False
                elif event.key == pg.K_f:
                    fire = False
                elif event.key == pg.K_v:
                    sas_angle = rocket.angle
                    auto = not auto

            elif event.type == pg.VIDEORESIZE:
                screen = pg.display.set_mode((event.w, event.h), pg.RESIZABLE)

            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 4:
                    Drawer._zoom /= 2
                elif event.button == 5:
                    if Drawer._zoom <= Drawer._maxZoom:
                        Drawer._zoom *= 2
                print("Zoom: {0}\n".format(Drawer._zoom))

        if fire:
            rocket.thrust(fireKey)
        if rotate:
            rocket.turn_SAS(rotKey, 1)
        if auto:
            rocket.auto_SAS(sas_angle)

        grav = updateGravity(space, rocket, celestialBodies, ticksPerSec)
        space.step(1/ticksPerSec)
        updateCamera(screen, Drawer.getOffset(screen, rocket))
        Drawer.drawMultiple(screen, space.shapes,
                            Drawer.getOffset(screen, rocket))
        Drawer.drawMultiple(screen, celestialBodies,
                            Drawer.getOffset(screen, rocket))
        pos = rocket.position
        vel = rocket.velocity
        hud.updateHUD(pos[0], pos[1], (math.degrees(rocket.angle)+90) % 360,
                      vel.length, vel.angle_degrees % 360,
                      grav.length, grav.angle_degrees % 360,
                      rocket.components, clock.get_fps())

        pg.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    run()
