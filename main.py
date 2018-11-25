import pygame
import sys
import os

pygame.init()
disp = pygame.display.set_mode((854, 480), pygame.RESIZABLE)

if os.path.exists(os.path.abspath("assets")):
    _ASSETS_PATH = os.path.abspath("assets")
elif os.path.exists(os.path.abspath("../assets")):
    _ASSETS_PATH = os.path.abspath("../assets")
    
from enum import Enum
from graphics import Menu
import simulationexec
from rocketbuilder import RocketBuilder


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
                pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

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
            else:
                menu.drawMenu(100)

        if currentState == State.Building:
            newRocket = RocketBuilder.run()
            if newRocket is not None:
                currentState = State.Playing
                rocket = newRocket


        if currentState == State.Playing:
            currentState = simulationexec.run(rocket)
            rocket =None

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    sys.exit()

main()
