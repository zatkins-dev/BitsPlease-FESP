from pygame.sprite import Sprite
import pygame


class Explosion(Sprite):
    def __init__(self, duration, images, *group):
        Sprite.__init__(self,*group)
        self.duration = duration
        self.size = 48,48
        self.rect = pygame.Rect((0,0),self.size)
        self.images = images
        self.current_frame = 0
        self.image = self.images[self.current_frame]

    def update_frame(self):
        self.current_frame += 1
        if self.current_frame >= len(self.images):
            self.current_frame = 0
        self.image = self.images[self.current_frame]

    def get_draw(self):
        if self.duration == 0:
            return None
        self.update_frame()
        self.duration -= 1
        return self.image

        