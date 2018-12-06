import pygame
import sys
import os

if os.path.exists(os.path.abspath("assets")):
    _ASSETS_PATH = os.path.abspath("assets")
elif os.path.exists(os.path.abspath("../assets")):
    _ASSETS_PATH = os.path.abspath("../assets")

from graphics import Video
disp = Video.get_display()

from enum import Enum
from graphics import Menu
from simulation import Simulation
from rocketbuilder import RocketBuilder

import unittest
import tests


def main():
    """
    The top level function for FESP. Ferries the program between the menu, the rocket builder, and the simulation.
    """
    pygame.display.set_icon(pygame.image.load(os.path.join(_ASSETS_PATH, "icon.png")))
    pygame.display.set_caption("FESP: The Flat Earth Space Program")
    menu = Menu()
    clock = pygame.time.Clock()
    State = menu.State

    currentState = State.Splash

    while currentState != State.Exit:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                currentState = State.Exit
            if event.type == pygame.VIDEORESIZE:
                Video.set_display(event.w,event.h)

        rocket = None

        if currentState == State.Splash:
            if menu.splashScreenPressed:
                currentState = State.Menu
                menu.splashScreenPressed = False
            else:
                menu.drawSplashScreen(100)

        if currentState == State.Menu:
            if menu.quitPressed:
                currentState = State.Exit
                menu.quitPressed = False
            elif menu.demoPressed:
                currentState = State.Playing
                menu.demoPressed = False
            elif menu.builderPressed:
                currentState = State.Building
                menu.builderPressed = False
            elif menu.testsPressed:
                currentState = State.Testing
                menu.testsPressed = False
            else:
                menu.drawMenu(100,tests=True)

        if currentState == State.Building:
            newRocket = RocketBuilder.run()
            if newRocket is not None:
                currentState = State.Playing
                rocket = newRocket

        if currentState == State.Testing:
            unittest.main(module="tests", verbosity=4, exit=False)
            currentState = State.Menu

        if currentState == State.Playing:
            currentState = Simulation.run(rocket)

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    sys.exit()

if __name__ == '__main__': main()
