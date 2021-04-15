import pygame
from x_animation import AnimationManager, Animation, StaticAnimation


class BlinkingAnimation(Animation):
    def __init__(self, image, duration=200):
        super().__init__([image, pygame.Surface(image.get_size(), pygame.SRCALPHA)],
                         duration,
                         is_looping=True)


class BlinkingAnimator(AnimationManager):
    __animations__ = {"normal": StaticAnimation, "blinking": BlinkingAnimation}

    def __init__(self, sprite_name, image, init_state="normal"):
        self.image = image
        super().__init__(sprite_name, None, self.__animations__, init_state)

    def __make_animation__(self, sprites, anim_name, anim_type):
        return anim_type(self.image)