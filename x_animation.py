import pygame

from x_sprite_factory import XSpriteFactory


class Animation(object):
    def __init__(self, images, durations, is_looping=False):
        if not isinstance(images, list):
            raise Exception()

        self.images = images
        self.is_looping = is_looping
        if not isinstance(durations, list):
            durations = [durations] * len(images)
        self.durations = durations

        self.current_frame = 0
        self.time_since_flip = 0

    def image(self):
        return self.images[self.current_frame]

    def flip(self):
        next_frame = self.current_frame + 1
        if next_frame == len(self.images):
            if self.is_looping:
                next_frame = 0
            else:
                next_frame -= 1
        self.current_frame = next_frame
        self.time_since_flip = 0

    def update(self, timedelta):
        self.time_since_flip += timedelta
        if self.time_since_flip >= self.durations[self.current_frame]:
            self.flip()

    def get_state(self):
        return (self.current_frame, len(self.images), self.time_since_flip)

    def set_state(self, new_state):
        frame, length, time = new_state
        if length != len(self.images):
            return
        self.current_frame, self.time_since_flip = frame, time

    def reset(self):
        self.current_frame = 0
        self.time_since_flip = 0


class BlinkingAnimation(Animation):
    def __init__(self, image, duration=100):
        super().__init__([image, pygame.Surface(image.get_size(), pygame.SRCALPHA)],
                         duration,
                         is_looping=True)


class StaticAnimation(Animation):
    def __init__(self, image, duration=0):
        super().__init__([image], duration)

    def update(self, timedelta):
        pass


class AnimationManager:
    @staticmethod
    def state_names(sprite_name, anim_dict):
        return zip(anim_dict.keys(), XSpriteFactory.anim_sprite_names(sprite_name, anim_dict))

    def __init__(self, sprite_name, sprites, anim_dict, init_state):
        self.animations = dict()
        self.state = None
        self.current_animation = None
        for state, anim_name in AnimationManager.state_names(sprite_name, anim_dict):
            self.animations[state] = self.__make_animation__(sprites, anim_name, anim_dict[state])
        self.set_state(init_state)

    def __make_animation__(self, sprites, anim_name, anim_type):
        return sprites[anim_name].make(anim_type)

    def set_state(self, new_state):
        if self.state != new_state:
            self.state = new_state
            self.change_animation()

    def change_animation(self):
        if self.current_animation:
            anim_state = self.current_animation.get_state()
            self.current_animation.reset()
            self.current_animation = self.__get_state_animation__()
            self.current_animation.set_state(anim_state)
        else:
            self.current_animation = self.__get_state_animation__()

    def __get_state_animation__(self):
        return self.animations[self.state]

    def current(self):
        return self.current_animation

    def update(self, timedelta):
        self.current_animation.update(timedelta)

