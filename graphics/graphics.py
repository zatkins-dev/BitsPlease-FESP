import pygame
from graphics.drawer import Drawer
import random

class Graphics(object):
    """
    Graphics contains a few very common graphics and UI components used in many places.
    """

    #: A state variable that stores whether a button is currently being pressed.
    #: This is used to prevent buttons' actions from executing on every single frame.
    _buttonIsClicked = False

    #: A state variable that stores whether the star background has been drawn before.
    #: Used to initialize the backgroudn on the first call of drawStars()
    _isBackgroundDrawn = False

    #: A list of tuples that hold information about stars. The first number
    #: is the x position, and the second number is the y position. The
    #: final member is an rgb color tuple.
    _stars = []

    #: The width of the stars Surface
    _starsWidth = 0
    #: THe height of the stars Surface
    _starsHeight = 0

    @classmethod
    def drawButton(cls, destSurf, pos, size, colors, buttonContent,
                   buttonContentSize, buttonFunction=None):
        """
        Utility function that draws a button to the screen

        :param destSurf: The Surface to draw the button onto.
        :type screen: :py:class:`pygame.Surface`
        :param pos: The positon of the top-left corner of the button
        :type pos: (int, int)
        :param size: The width and height respectively of the button
        :type size: (int, int)
        :param colors: A tuple containing two colors. The first is the unfocused color, and the second is the focused color
        :type colors: (:py:class:`pygame.Color`, :py:class:`pygame.Color`)
        :param buttonContent: This can be either a surface or a string. Either will be drawn to the center of the button
        :type buttonContent: :py:class:`pygame.Surface` or :py:class:`string`
        :param buttonContentSize: If the button content is a string, this will be the size of font used to render the text. If the content is a surface, this is the ammount of the button the surface will occupy, from 0 to 1
        :param buttonFunction: This is the function that will be executed when the button is clicked on.
        :type buttonFunction: :py:class:`types.FunctionType`
        """

        if type(buttonContent) is pygame.Surface:
            #find the size of the sprite within the button
            newWidth = int(buttonContentSize * size[0])
            newHeight = int(buttonContentSize * size[1])

            #scale the sprite to fit within the button
            if buttonContent.get_width() > buttonContent.get_height():
                ratio = buttonContent.get_height() / buttonContent.get_width()
                content = pygame.transform.scale(buttonContent, (newWidth, int(newHeight * ratio)))
            elif buttonContent.get_width() < buttonContent.get_height():
                ratio =  buttonContent.get_width() / buttonContent.get_height()
                content = pygame.transform.scale(buttonContent, (int(newWidth * ratio), newHeight))
            else:
                content = pygame.transform.scale(buttonContent, (newWidth, newHeight))

        else:
            if(not pygame.font.get_init()):
                pygame.font.init()
            t_font = pygame.font.SysFont('lucidaconsole', int(buttonContentSize))
            content = t_font.render(str(buttonContent), True, (255, 255, 255))

        button = pygame.surface.Surface(size, pygame.constants.SRCALPHA)

        offset = destSurf.get_abs_offset()

        # see if mouse is within the area of our button
        mousePos = pygame.mouse.get_pos()
        if mousePos[0] > pos[0] + offset[0] \
           and mousePos[0] < pos[0] + size[0] + offset[0] \
           and mousePos[1] > pos[1] + offset[1] \
           and mousePos[1] < pos[1] + size[1] + offset[1]:
            # mouse is over the button
            button.fill(colors[1])
            # mouse is in the button, so it may click the
            # button and run its function
            if pygame.mouse.get_pressed()[0] \
               and buttonFunction is not None \
               and not cls._buttonIsClicked:
                buttonFunction()
                cls._buttonIsClicked = True
            elif not pygame.mouse.get_pressed()[0] and cls._buttonIsClicked:
                cls._buttonIsClicked = False
        else:
            # mouse isn't in the button
            button.fill(colors[0])

        # put button onto the screen,
        # then text onto the screen centered over the button
        destSurf.blits([
            (button, pos),
            (content, (pos[0] + size[0] / 2 - content.get_width() / 2,
                    pos[1] + size[1] / 2 - content.get_height() / 2))
        ])

    @classmethod
    def drawText(cls, position, content, textFont, color=(0, 0, 0),
                 surface=None):
        """
        Utility function that draws a string to the screen

        :param position: The XY position of the top-left corner of the text
        :type position: (int, int)
        :param string content: The string the be drawn 
        :param textFont: The font to use to render the text. 
        :type textFont: :py:class:`pygame.font.Font`
        :param color: The rgb color of the text
        :type color: :py:class:`pygame.Color`
        :param surface: The surface to draw to
        :type surface: :py:class:`pygame.Surface`
        """
        if surface is None:
            surface = pygame.display.get_surface()
        if(not pygame.font.get_init()):
            pygame.font.init()

        textSurface = textFont.render(str(content), True, color)

        surface.blit(textSurface, position)

    @classmethod
    def drawTextCenter(cls, position, content, textFont, color=(0, 0, 0),
                       surface=None):
        """
        Utility function that draws a string to the screen

        :param position: The XY position of the center of the text
        :type position: (int, int)
        :param str content: The string the be drawn 
        :param textFont: The font to use to render the text. 
        :type textFont: :py:class:`pygame.font.Font`
        :param color: The rgb color of the text
        :type color: :py:class:`pygame.Color`
        :param surface: The surface to draw to
        :type surface: :py:class:`pygame.Surface`
        """
        if surface is None:
            surface = pygame.display.get_surface()
        if(not pygame.font.get_init()):
            pygame.font.init()

        textSurface = textFont.render(str(content), True, color)
        x, y = textSurface.get_size()

        x = position[0] - x/2
        y = position[1] - y/2

        surface.blit(textSurface, (x, y))

    @classmethod
    def drawStars(cls, screen, pos):
        """
        Draws a randomly generated background of stars to the provided surface.
        Also creates a paralax effect for a moving target

        :param screen: The :py:class:`pygame.Surface` to draw to.
        :type screen: :py:class:`pygame.Surface`
        :param pos: The position of the rocket, used to offset the stars and create a parallax effect.
        :type pos: (float, float)
        """

        w, h = screen.get_size()
        if (cls._starsWidth != w):
            cls._isBackgroundDrawn = False
            cls._starsWidth = w
            cls._stars.clear()
        if (cls._starsHeight != h):
            cls._isBackgroundDrawn = False
            cls._starsHeight = h
            cls._stars.clear()

        if(not cls._isBackgroundDrawn):
            for i in range(1000):
                colorSelector = random.randrange(0, 5)
                colorStar = (0, 0, 0)
                if(colorSelector == 0 or colorSelector == 1):
                    colorStar = (255, 255, 255)
                elif(colorSelector == 2):
                    colorStar = (255, 0, 0)
                elif(colorSelector == 3):
                    colorStar = (0, 0, 255)
                elif(colorSelector == 4):
                    colorStar = (255, 255, 0)
                x = random.randrange(0, cls._starsWidth)
                y = random.randrange(0, cls._starsHeight)
                cls._stars.append([x, y, colorStar])
            cls._isBackgroundDrawn = True
        for i in range(min(int(1000 / Drawer.zoom.zoom), 1000)):
            # decide the new star size (twinkling)
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

            paralaxModifier = .05 * Drawer.zoom.zoom

            starX = int(cls._stars[i][0] + paralaxModifier * pos[0]) % cls._starsWidth
            starY = int(cls._stars[i][1] - paralaxModifier * pos[1]) % cls._starsHeight
            pygame.draw.circle(screen, cls._stars[i][2], (starX, starY), width)
