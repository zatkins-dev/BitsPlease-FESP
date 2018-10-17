import pygame
import pymunk
import sys
from enum import Enum
from Graphics.menu import menu
import ExecutePhysics

def main():
    clock = pygame.time.Clock()
    State = Enum('State', 'Splash Menu Playing Exit')

    currentState = State.Splash

    pygame.display.set_mode((854, 480), pygame.RESIZABLE)

    while currentState != State.Exit:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                currentState = State.Exit
            if event.type == pygame.VIDEORESIZE:
                pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

        if currentState == State.Splash:
            if menu.splashScreenPressed:
                currentState = State.Menu
                menu.splashScreenPressed = False
            else:
                menu.drawSplashScreen()

        if currentState == State.Menu:
            if menu.quitPressed:
                currentState = State.Exit
                menu.quitPressed = False
            elif menu.demoPressed:
                currentState = State.Playing
                menu.demoPressed = False
            else:
                menu.drawMenu()

        if currentState == State.Playing:
            ExecutePhysics.run()

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    sys.exit()

main()
            