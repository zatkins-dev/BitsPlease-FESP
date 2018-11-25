import pygame as pg
import pymunk as pm
from rockets import Rocket, UpGoer2000, LeftRCS, RightRCS, CommandModule, AdvancedSAS

import os
import sys

def genRocket(space):
    """
    Generate prototype rocket with orbiter, thruster, and SAS.

    :param space:  Space to hold generated rocket.
    :type space: :py:class:`pymunk.Space`
    """
    rocket = Rocket([UpGoer2000(None), AdvancedSAS(None), CommandModule(None), LeftRCS(None), RightRCS(None)])
    space.add(rocket)
    for c in rocket.components:
        space.add(c)
    return rocket
