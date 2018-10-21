import pygame as pg
from rockets import Component
from rockets import Thruster
from rockets import SAS
from rockets import Rocket


def genOrbiter(b):
    """Generate new component (orbiter).

    Args:
        b (Body): Rocket body to attach to.

    Returns:
        Component: Orbiter component for prototype rocket.

    """
    density = 34
    verts = [(12, 4), (-12, 4), (0, 42)]
    orbiter = Component(b, verts, radius=1)
    orbiter.density = density
    return orbiter


def genTank(b):
    """Generate new thruster for rocket.

    Args:
        b (Body): Rocket body to attach to.

    Returns:
        Thruster: Thruster for prototype rocket.

    """
    verts = [(4.2, 0), (-4.2, 0), (4.2, 46.9), (-4.2, 46.9)]
    density = 73.58
    tank = Thruster(b, verts, (0, 1), 100000, radius=1)
    tank.density = density
    tank.key = pg.K_f
    return tank


def genSAS(b):
    """Generate new SAS for prototype rocket.

    Args:
        b (Body): Rocket body to attach to.

    Returns:
        SAS: SAS for prototype rocket.

    """
    density = 100
    verts = [(3, 6), (-3, 6), (-3, 12), (3, 12)]
    sas = SAS(b, verts, 0.05, 0, radius=1)
    sas.density = density
    sas.leftKey = pg.K_a
    sas.rightKey = pg.K_d
    return sas


def genRocket(space):
    """Generate prototype rocket with orbiter, thruster, and SAS.

    Args:
        space (Space): Space to hold generated rocket.

    Returns:
        Rocket: Generated prototype rocket.

    """
    rocket = Rocket()
    components = [genTank(rocket), genSAS(rocket), genOrbiter(rocket)]
    for c in components:
        rocket.addComponent(c)
    space.add(rocket)
    for c in components:
        space.add(c)
    return rocket
