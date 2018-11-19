import pygame as pg
import pymunk as pm
from rockets import *

import os
import sys


def genOrbiter(b):
    """Generate new component (orbiter).

    Args:
        b (Body): Rocket body to attach to.

    Returns:
        Component: Orbiter component for prototype rocket.

    """
    orbiter = CommandModule(b, radius=1)
    return orbiter


def genTank(b):
    """Generate new thruster for rocket.

    Args:
        b (Body): Rocket body to attach to.

    Returns:
        Thruster: Thruster for prototype rocket.

    """
    tank = UpGoer2000(b, radius=1)
    return tank


def genSAS(b):
    """Generate new SAS for prototype rocket.

    Args:
        b (Body): Rocket body to attach to.

    Returns:
        SAS: SAS for prototype rocket.

    """
    sas = AdvancedSAS(b)
    return sas

def genRocket(space):
    """Generate prototype rocket with orbiter, thruster, and SAS.

    Args:
        space (Space): Space to hold generated rocket.

    Returns:
        Rocket: Generated prototype rocket.

    """
    rocket = Rocket()
    rocket.components = [genTank(rocket), genSAS(rocket), genOrbiter(rocket), LeftRCS(rocket), RightRCS(rocket)]
    space.add(rocket)
    for c in rocket.components:
        space.add(c)
    return rocket
