import pygame as pg
import pymunk as pm
import pymunk.pygame_util as pygame_util
from pymunk.vec2d import Vec2d
import random


def genOrbiter(body):
    density = 34
    verts = [(12, 4), (-12, 4), (0, 42)]
    orbiter = pm.Poly(body, verts, radius=1)
    orbiter.density = density
    return orbiter


def genTank(body):
    verts = [(4.2, 0), (-4.2, 0), (4.2, 46.9), (-4.2, 46.9)]
    density = 73.58
    tank = pm.Poly(body, verts, radius=1)
    tank.density = density
    return tank


def genRocket(space):
    body = pm.Body()
    components = [genTank(body), genOrbiter(body)]
    space.add(body)
    for c in components:
        space.add(c)
    return body


def getRocketThrust(rocket, netThrust):
    angle = rocket.rotation_vector
    # random.seed()
    angle_perturbation = random.normalvariate(0, 0.001)
    thrust = Vec2d(0, netThrust)
    print("original: {0}\n", thrust)
    thrust.cpvrotate(angle)
    print("based on ship angle: {0}\n", thrust)
    thrust.rotate(angle_perturbation)
    print("perturbed: {0}\n", thrust)
    return thrust
