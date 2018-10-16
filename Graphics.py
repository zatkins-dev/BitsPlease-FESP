class Graphics(object):
    
    _buttonIsClicked = False

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
    t_font = font.SysFont('lucidaconsole', buttonTextSize)
    text = t_font.render(str(buttonText), True, (0,0,0))

    button = surface.Surface(size, constants.SRCALPHA)

    offset = destSurf.get_abs_offset()

    #see if mouse is within the area of our button
    mousePos = mouse.get_pos()
    if mousePos[0] > pos[0] + offset[0] and mousePos[0] < pos[0] + size[0] + offset[0] and mousePos[1] > pos[1] + offset[1] and mousePos[1] < pos[1] + size[1] + offset[1]:
        #mouse is over the button
        button.fill(colors[1])
        #mouse is in the button, so it may click the button and run its function
        if mouse.get_pressed()[0] and buttonFunction != None and not cls._buttonIsClicked:
            buttonFunction()
            cls._buttonIsClicked = True
        elif not mouse.get_pressed()[0] and cls._buttonIsClicked:
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
    def drawText(cls, position, content, size=20, color=(0,0,0), font='lucidaconsole', surface=pygame.display.get_surface()):
        textFont = font.SysFont('lucidaconsole', size)
        textSurface = textFont.render(str(content), True, color)
        x, y = pygame.display.get_surface().get_size()

        x = x - textSurface.get_width() / 2
        y = y - textSurface.get_height() / 2

        surface.blit(textSurface, (x,y))