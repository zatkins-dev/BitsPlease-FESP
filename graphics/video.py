import pygame


class Video:
    """
    Handler for the pygame display, does hardware accelerations 
    """
    #: Fullscreen size
    __screen_width, __screen_height = 0, 0
    #: Current size or size before fullscreen
    __width, __height = 854, 480
    #: Bool to store if display is fullscreen
    __fullscreen = False
    #: Bool to store if display has been initialized
    __initialized = False

    @classmethod
    def init(cls):
        """
        Initializes the display and stores the monitor/screen size.
        """
        if not cls.__initialized:
            pygame.init()
            info = pygame.display.Info()
            cls.__screen_width,cls.__screen_height = info.current_w,info.current_h
            cls.set_display(cls.__width, cls.__height)
            cls.__initialized = True
        
            

    @classmethod
    def set_display(cls, w, h):
        """
        Sets the size of the active display to `w` by `h`. If new dimensions are fullscreen, enables fullscreen hardware acceleration.

        :param int w: New width
        :param int h: New height
        """

        if w == cls.__screen_width and h == cls.__screen_height:
            pygame.display.set_mode((w, h), pygame.FULLSCREEN or pygame.HWSURFACE or pygame.OPENGL or pygame.DOUBLEBUF)
        else:
            cls.__width, cls.__height = w, h
            pygame.display.set_mode((cls.__width, cls.__height), pygame.RESIZABLE or pygame.OPENGL or pygame.DOUBLEBUF)

    @classmethod
    def get_display(cls):
        """
        Gets the active display

        :returns: Current display
        :rtype: :py:class:`pygame.Surface`
        """
        if not cls.__initialized:
            cls.init()
        return pygame.display.get_surface()

    @classmethod
    def toggle_fullscreen(cls):
        """
        Toggles the display fullscreen
        """
        cls.__fullscreen = not cls.__fullscreen
        if cls.__fullscreen:
            cls.set_display(cls.__screen_width, cls.__screen_height)
        else:
            cls.set_display(cls.__width, cls.__height)

    @classmethod
    def get_fullscreen(cls):
        """
        Returns whether the screen is fullscreen

        :returns: Current state of fullscreen
        :rtype: bool
        """

        return cls.__fullscreen