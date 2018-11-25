from pygame.sprite import Sprite
import pygame


class Explosion(Sprite):
    """
    Create a new explosion animation

    :param int duration: number of ticks for which to display the explosion animation 
    :param images: array of animation frames
    :type images: [:py:class:`pygame.Surface`]
    """

    def __init__(self, duration, images, *group):
        Sprite.__init__(self,*group)
        #: number of ticks for animation
        self.duration = duration

        #: size of explosion sprite
        self.size = 48,48

        #: rectangle containing the surface of the sprite
        self.rect = pygame.Rect((0,0),self.size)

        #: Animation frames passed from `images`
        self.images = images

        #: Current frame step in animation
        self.current_frame = 0

        #: Current displayed image
        self.image = self.images[self.current_frame]

    def update_frame(self):
        """
        Updates :py:attr:`image` to the next frame of the animation, looping around once the final frame is reached.
        """

        self.current_frame += 1
        if self.current_frame >= len(self.images):
            self.current_frame = 0
        self.image = self.images[self.current_frame]

    def get_draw(self):
        """
        Gets the current animation image if duration is non-zero.

        :returns: :py:attr:`image` or `None`
        :rtype: :py:class:`pygame.Surface`
        """

        if self.duration == 0:
            return None
        self.update_frame()
        self.duration -= 1
        return self.image

        