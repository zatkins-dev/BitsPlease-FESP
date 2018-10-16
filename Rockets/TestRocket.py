import pygame as pg
<<<<<<< HEAD:Rockets/TestRocket.py
from Rockets.component import Component
from Rockets.thruster import Thruster
from Rockets.rocket import Rocket
=======
from component import Component
from thruster import Thruster
from SAS import SAS
from rocket import Rocket
>>>>>>> SAS-module:Physics/TestRocket.py


def genOrbiter(b):
    density = 34
    verts = [(12, 4), (-12, 4), (0, 42)]
    orbiter = Component(b, verts, radius=1)
    orbiter.density = density
    return orbiter


def genTank(b):
    verts = [(4.2, 0), (-4.2, 0), (4.2, 46.9), (-4.2, 46.9)]
    density = 73.58
<<<<<<< HEAD:Rockets/TestRocket.py
    tank = Thruster(b, verts, (0, 1), 100000, radius=1)
    #5255000
=======
    tank = Thruster(b, verts, (0, 1), 100000, radius=1) 
>>>>>>> SAS-module:Physics/TestRocket.py
    tank.density = density
    tank.key = pg.K_f
    return tank

def genSAS(b):
    density = 30
    verts = [(3,3), (-3, 3), (-3, 9), (3, 9)]
    sas = SAS(b, verts, 0, 0.05, 0, radius=1)
    sas.density = density
    sas.leftKey = pg.K_a
    sas.rightKey = pg.K_d
    return sas

def genRocket(space):
    rocket = Rocket()
    components = [genTank(rocket), genSAS(rocket), genOrbiter(rocket)]
    for c in components:
        rocket.addComponent(c)
    space.add(rocket)
    for c in components:
        space.add(c)
    return rocket
