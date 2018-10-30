import pygame as pg
import pymunk as pm
import pymunk.pygame_util as pygame_util
import sys
import rockets.testrocket as tr
import math
from physics import CelestialBody as cb
from physics import Physics as phy
from graphics import HUD
from graphics import Graphics as graph
from graphics import Drawer

res_x, res_y = 1000, 1000
GROUND_Y = res_y/20
G = 6.67408*10**-11


def keyDown(e, key):
    return e.type == pg.KEYDOWN and e.key == key


def keyUp(e, key):
    return e.type == pg.KEYUP and e.key == key


def updateGravity(space, rocket, objects):
    space.gravity = phy.netGravity(objects, rocket)
    space.gravity[0] = space.gravity[0]/rocket.mass
    space.gravity[1] = space.gravity[1]/rocket.mass


def updateCamera(screen, center):
    screen.fill((0, 0, 0))
    graph.drawStars(screen, center)


def run():
    celestialBodies = []
    screen = pg.display.get_surface()
    clock = pg.time.Clock()

    game = pg.Surface((10000, 10000))

    space = pm.Space()
    hud = HUD()

    earth = cb('earth', space, 10**13, 1000, 5000, 5000, 0.9, 0, 0)
    celestialBodies.append(earth)

    earthMoon1 = cb('earthMoon1', space, 10**11, 250, 6500, 5000, 0.9, 0, 1)
    celestialBodies.append(earthMoon1)

    planetGage = cb('planetGage', space, 10**12, 200, 1000, 1000, 0.9, 0, 0)
    celestialBodies.append(planetGage)

    planetThomas = cb('planetThomas', space, 10**13, 200, 1500, 1500, .9, 0, 0)
    celestialBodies.append(planetThomas)

    planetZach = cb('planetZach', space, 10**13, 200, 2000, 1000, 0.9, 0, 0)
    celestialBodies.append(planetZach)

    rocket = tr.genRocket(space)
    x, y = (earth.posx + earth.radius / math.sqrt(2),
            earth.posy + earth.radius / math.sqrt(2))
    rocket.position = x, y
    # draw_options = pygame_util.DrawOptions(game)
    space.damping = 0.9

    fire_ticks = 480*50
    fire = False
    rotate = False
    auto = False
    sas_angle = 0

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

        if fire:
            fire_ticks -= 1
            rocket.thrust(fireKey)
        if rotate:
            rocket.turn_SAS(rotKey, 1)
        if auto:
            rocket.auto_SAS(sas_angle)

        updateGravity(space, rocket, celestialBodies)
        space.step(1/50.0)
        updateCamera(screen, Drawer.getOffset(screen, rocket))
        Drawer.drawMultiple(screen, list(map(lambda x: x.shape, celestialBodies)), 
                            Drawer.getOffset(screen, rocket))
        Drawer.drawMultiple(screen, rocket.components,
                            Drawer.getOffset(screen, rocket))
        print(Drawer.to_pygame(rocket.components[0], rocket.position, Drawer.getOffset(screen, rocket)))
        pos = rocket.position
        vel = rocket.velocity
        grav = space.gravity
        hud.updateHUD(pos[0], pos[1], (math.degrees(rocket.angle)+90) % 360,
                      vel.length, vel.angle_degrees % 360,
                      grav.length, grav.angle_degrees % 360,
                      rocket.components, clock.get_fps())

        pg.display.flip()
        clock.tick(30)


if __name__ == "__main__":
    run()
