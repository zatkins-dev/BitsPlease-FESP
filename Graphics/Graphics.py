import pygame
import random

class Graphics(object):

    _buttonIsClicked = False
    _isBackgroundDrawn = False
    _stars = []

    @classmethod
    def drawButton(cls, destSurf, pos, size, colors, buttonText, buttonTextSize, buttonFunction=None):
        """
        Utility function that draws a button to the screen

        **Args**:
                *destSurf*: Surface The surface that the button will be drawn to

                *pos*: Tuple (int, int) The (x,y) position of the button. This point corresponds to the top-left corner of the button.

                *size*: Tuple (int, int) The (width, height) of the button to be drawn.

                *colors*: Tuple (Color, Color) The first member of the tuple is the color of the button, and the second
                    member is the color of the button while it is being hovered over. These colors can be given as
                    pygame colors, triples of RGB values, or 4-tuples of RGBA values if transparency is desired

                *buttonText*: The text to be rendered at the center of the button

                *buttonTextSize*: The size of the text to be rendered

                *buttonFunction*: A function to call while the button is pressed

        **Preconditions**:
                None.

        **Postconditions**:
                None.

        **Returns**: None.
        """
        if(not pygame.font.get_init()):
            pygame.font.init()
        t_font = pygame.font.SysFont('lucidaconsole', buttonTextSize)
        text = t_font.render(str(buttonText), True, (255,255,255))

        button = pygame.surface.Surface(size, pygame.constants.SRCALPHA)

        offset = destSurf.get_abs_offset()

        #see if mouse is within the area of our button
        mousePos = pygame.mouse.get_pos()
        if mousePos[0] > pos[0] + offset[0] and mousePos[0] < pos[0] + size[0] + offset[0] and mousePos[1] > pos[1] + offset[1] and mousePos[1] < pos[1] + size[1] + offset[1]:
            #mouse is over the button
            button.fill(colors[1])
            #mouse is in the button, so it may click the button and run its function
            if pygame.mouse.get_pressed()[0] and buttonFunction != None and not cls._buttonIsClicked:
                buttonFunction()
                cls._buttonIsClicked = True
            elif not pygame.mouse.get_pressed()[0] and cls._buttonIsClicked:
                cls._buttonIsClicked = False
        else:
            #mouse isn't in the button
            button.fill(colors[0])

        #put button onto the screen, then text onto the screen centered over the button
        destSurf.blits([
            (button, pos),
            (text, (pos[0] + size[0] / 2 - text.get_width() / 2, pos[1] + size[1] / 2 - text.get_height() / 2))
        ])

    @classmethod
    def drawText(cls, position, content, size=20, color=(0,0,0), font='lucidaconsole', surface=None):
        if surface == None:
            surface = pygame.display.get_surface()
        if(not pygame.font.get_init()):
            pygame.font.init()

        textFont = pygame.font.SysFont('lucidaconsole', size)
        textSurface = textFont.render(str(content), True, color)
        x, y = textSurface.get_size()

        x = position[0] - x/2
        y = position[1] - y/2

        surface.blit(textSurface, (x,y))

    @classmethod
    def drawStars(cls, screen, pos):
        if(not cls._isBackgroundDrawn):
            for i in range(1000):
                colorSelector = random.randrange(0, 5)
                colorStar = (0,0,0)
                if(colorSelector == 0 or colorSelector == 1):
                    colorStar = (255, 255, 255)
                elif(colorSelector == 2):
                    colorStar = (255, 0, 0)
                elif(colorSelector == 3):
                    colorStar = (0, 0, 255)
                elif(colorSelector == 4):
                    colorStar = (255, 255, 0)
                x = random.randrange(0, 3000)
                y = random.randrange(0, 1080)
                cls._stars.append([x,y,colorStar])
            cls._isBackgroundDrawn = True
        for i in range(1000):
            #decide the new star size (twinkling)
            temp = random.uniform(0, 1)
            width = 0
            if temp < .01:
                width = 0
            elif temp < .98:
                width = 1
            elif temp < .99:
                width = 2
            else:
                width = 3

            starX = int(cls._stars[i][0] - .25 * pos[0]) % 3000
            starY = int(cls._stars[i][1] + .25 * pos[1]) % 1080
            pygame.draw.circle(screen, cls._stars[i][2], (starX, starY), width)
