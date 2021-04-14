from x_animation import AnimationManager, StaticAnimation, BlinkingAnimation


class BlinkingAnimator(AnimationManager):
    __animations__ = {"normal": StaticAnimation, "blinking": BlinkingAnimation}

    def __init__(self, sprite_name, image, init_state="normal"):
        self.image = image
        super().__init__(sprite_name, None, self.__animations__, init_state)

    def __make_animation__(self, sprites, anim_name, anim_type):
        return anim_type(self.image)