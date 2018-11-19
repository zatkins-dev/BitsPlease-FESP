import pygame
import sys
from enum import Enum
from graphics import Menu
import simulationexec
from rocketbuilder import RocketBuilder


def main():
    menu = Menu()
    clock = pygame.time.Clock()
    State = menu.State

    currentState = State.Splash
    disp = pygame.display.set_mode((854, 480), pygame.RESIZABLE and pygame.SRCALPHA )

    while currentState != State.Exit:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                currentState = State.Exit
            if event.type == pygame.VIDEORESIZE:
                pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE and pygame.SRCALPHA)

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
            RocketBuilder.run()

        if currentState == State.Playing:
            currentState = simulationexec.run()

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    sys.exit()

main()
