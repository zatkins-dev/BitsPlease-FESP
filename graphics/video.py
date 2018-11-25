import pygame


class Video:
    __screen_width,__screen_height = 0,0
    __initialized = False

    @classmethod
    def init(cls):
        if not cls.__initialized:
            pygame.init()
            info = pygame.display.Info()
            cls.__screen_width,cls.__screen_height = info.current_w,info.current_h
            pygame.display.set_mode((854, 480), pygame.RESIZABLE or pygame.OPENGL or pygame.DOUBLEBUF)
            cls.__initialized = True

    @classmethod
    def set_display(cls, w, h):
        if w == cls.__screen_width and h == cls.__screen_height:
            pygame.display.set_mode((w, h), pygame.FULLSCREEN or pygame.HWSURFACE or pygame.OPENGL or pygame.DOUBLEBUF)
        else:
            pygame.display.set_mode((w, h), pygame.RESIZABLE or pygame.OPENGL or pygame.DOUBLEBUF)

    @classmethod
    def get_display(cls):
        if not cls.__initialized:
            cls.init()
        return pygame.display.get_surface()
