import pygame as pg
import pymunk as pm
import pymunk.pygame_util as pygame_util
from pymunk.vec2d import Vec2d
import sys
import TestRocket as tr
import math

res_x, res_y = 1000, 1000
EARTH_MASS = 5.97*10**24
EARTH_RADIUS = 6371000
EARTH_MOMENT = pm.moment_for_circle(EARTH_MASS, 0, EARTH_RADIUS)
GROUND_Y = res_y/20
G = 6.67408*10**-11

def keyDown(e, key):
    return e.type == pg.KEYDOWN and e.key == key

def keyUp(e, key):
    return e.type == pg.KEYUP and e.key == key

def updateGravity(space, rocket, ground):
    r_sqrd = rocket.position[1]**2
    space.gravity = (0, -G*ground.mass*rocket.mass/r_sqrd)


def run():
    pg.init()
    screen = pg.display.set_mode((res_x, res_y))
    clock = pg.time.Clock()

    space = pm.Space()
    # earthBody = pm.Body(EARTH_MASS, EARTH_MOMENT, pm.Body.STATIC)
    groundLine = pm.Segment(
        space.static_body, (0, GROUND_Y), (1000, GROUND_Y), 50
    )
    groundLine.mass = EARTH_MASS
    space.add(groundLine)
    rocket = tr.genRocket(space)
    x, y = math.floor(res_x/2), math.floor(GROUND_Y)
    rocket.position = x, y
    draw_options = pygame_util.DrawOptions(screen)
    space.gravity = 0, -9.8
    space.damping = 0.9
    fire_ticks = 480*50
    fire = False
    rotate = False
    
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT or keyDown(event, pg.K_ESCAPE):
                sys.exit(0)
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_a or event.key == pg.K_d :
                    rotKey = event.key
                    rotate = True  
                elif event.key == pg.K_f :
                    fireKey = event.key
                    fire = True
        
            elif event.type == pg.KEYUP:
                if event.key == pg.K_a or event.key == pg.K_d :
                    rotate = False  
                elif event.key == pg.K_f :
                    fire = False          

        if fire:
            fire_ticks -= 1
            rocket.thrust(fireKey)
        if rotate:
            rocket.rotate(rotKey)
            
        print(space.gravity)
        # updateGravity(space, rocket, groundLine)
        space.step(1/50.0)
        screen.fill((255, 255, 255))
        space.debug_draw(draw_options)
        pg.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    run()
