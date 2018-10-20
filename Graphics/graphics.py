import pygame
import random

class Graphics(object):
    """
        Graphics is a utility class that is used to abstract drawing of different common items, like text and buttons

        **Class Variables**:
            *_buttonIsClicked*:     bool A state variable that stores whether a button is currently being pressed. This is used to prevent buttons' actions from executing on every single frame.
            
            *_isBackgroundDrawn*:   bool A state variable that stores whether or not the star background has been drawn before. This is used to initialize the backgroudn on the first call of drawStars()
            
            *_stars*:               tuple (int, int, (int, int, int)) A list of tuples that hold information about stars. The first number is the x position, and the second number is the y position. The final member is an rgb color tuple.
    """

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
    def drawText(cls, position, content, textFont, color=(0,0,0), surface=None):
        """
        Utility function that draws a string to the screen

        **Args**:
                *position*: Tuple (int, int) The (x,y) pixel coordinate of the top-left corner of the text

                *content*: str The string to be drawn

                *textFont*: pygame.font The font to use to draw the text

                *color*: Tuple (r,g,b) The rgb color values of the text to draw

                *surface*: The surface to draw to. Defaults to pygame's base surface

        **Preconditions**:
                None.

        **Postconditions**:
                None.

        **Returns**: None.
        """
        if surface == None:
            surface = pygame.display.get_surface()
        if(not pygame.font.get_init()):
            pygame.font.init()

        textSurface = textFont.render(str(content), True, color)

        surface.blit(textSurface, position)
        
    @classmethod
    def drawTextCenter(cls, position, content, textFont, color=(0,0,0), surface=None):
        """
        Utility function that draws a string to the screen

        **Args**:
                *position*: Tuple (int, int) The (x,y) pixel coordinate of the center of the text

                *content*: str The string to be drawn

                *textFont*: pygame.font The font to use to draw the text

                *color*: Tuple (r,g,b) The rgb color values of the text to draw

                *surface*: The surface to draw to. Defaults to pygame's base surface

        **Preconditions**:
                None.

        **Postconditions**:
                None.

        **Returns**: None.
        """
        if surface == None:
            surface = pygame.display.get_surface()
        if(not pygame.font.get_init()):
            pygame.font.init()

        textSurface = textFont.render(str(content), True, color)
        x, y = textSurface.get_size()

        x = position[0] - x/2
        y = position[1] - y/2

        surface.blit(textSurface, (x,y))

    @classmethod
    def drawStars(cls, screen, pos):
        """
        Draws a randomly generated background of stars to the provided surface. Also creates a paralax effect for a moving target

        **Args**
            *screen*:   pygame.Surface The surface which the stars will be drawn to

            *pos*:      tuple (int, int) The position of the focus of the camera, which will shift the position of the stars creating the paralax effect
            
        **Preconditions**:
                None.

        **Postconditions**:
                None.

        **Returns**: None.
        """
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