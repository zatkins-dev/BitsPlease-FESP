from pygame.sprite import Sprite
import pygame


class Explosion(Sprite):
    def __init__(self, *group):
        super(Explosion, self).__init__(*group)
        size = 10,10
        self.rect = pygame.Rect((0,0),size)
        self.images = []
        for i in range(5):
            self.images.append(pygame.image.load("/Users/Zach/Repos/BitsPlease-FESP/assets/sprites/explosion"+str(i+1)+".png").convert_alpha())
        self.current_frame = 0
        self.image = self.images[self.current_frame]

    def update_frame(self):
        self.current_frame += 1
        if self.current_frame >= len(self.images):
            self.current_frame = 0
        self.image = self.images[self.current_frame]
        