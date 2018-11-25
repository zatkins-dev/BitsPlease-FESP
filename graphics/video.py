import pygame


class Video:
    """
    Handler for the pygame display, does hardware accelerations 
    """
    __screen_width, __screen_height = 0, 0
    __width, __height = 854, 480
    __fullscreen = False
    __initialized = False

    @classmethod
    def init(cls):
        if not cls.__initialized:
            pygame.init()
            info = pygame.display.Info()
            cls.__screen_width,cls.__screen_height = info.current_w,info.current_h
            cls.set_display(cls.__width, cls.__height)
            cls.__initialized = True
        
            

    @classmethod
    def set_display(cls, w, h):
        if w == cls.__screen_width and h == cls.__screen_height:
            pygame.display.set_mode((w, h), pygame.FULLSCREEN or pygame.HWSURFACE or pygame.OPENGL or pygame.DOUBLEBUF)
        else:
            cls.__width, cls.__height = w, h
            pygame.display.set_mode((cls.__width, cls.__height), pygame.RESIZABLE or pygame.OPENGL or pygame.DOUBLEBUF)

    @classmethod
    def get_display(cls):
        if not cls.__initialized:
            cls.init()
        return pygame.display.get_surface()

    @classmethod
    def toggle_fullscreen(cls):
        cls.__fullscreen = not cls.__fullscreen
        if cls.__fullscreen:
            cls.set_display(cls.__screen_width, cls.__screen_height)
        else:
            cls.set_display(cls.__width, cls.__height)

    @classmethod
    def get_fullscreen(cls):
        return cls.__fullscreen