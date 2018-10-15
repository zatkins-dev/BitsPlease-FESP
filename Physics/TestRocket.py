import pygame as pg
from component import Component
from thruster import Thruster
from rocket import Rocket


def genOrbiter(b):
    density = 34
    verts = [(12, 4), (-12, 4), (0, 42)]
    orbiter = Component(b, verts, radius=1)
    orbiter.density = density
    return orbiter


def genTank(b):
    verts = [(4.2, 0), (-4.2, 0), (4.2, 46.9), (-4.2, 46.9)]
    density = 73.58
    tank = Thruster(b, verts, (0, 1), 100000, radius=1) 
    #5255000
    tank.density = density
    tank.key = pg.K_f
    return tank


def genRocket(space):
    rocket = Rocket()
    components = [genTank(rocket), genOrbiter(rocket)]
    for c in components:
        rocket.addComponent(c)
    space.add(rocket)
    for c in components:
        space.add(c)
    return rocket
