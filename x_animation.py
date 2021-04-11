import pygame


class Animation(object):
    def __init__(self, images, durations, is_looping=False):
        if not isinstance(images, list):
            raise Exception()

        self.images = images
        self.is_looping = is_looping
        if not isinstance(durations, list):
            durations = [durations] * len(images)
        self.durations = durations

        self.current_id = 0
        self.time_since_flip = 0

    def image(self):
        return self.images[self.current_id]

    def flip(self):
        next_id = self.current_id + 1
        if next_id == len(self.images):
            if self.is_looping:
                next_id = 0
            else:
                next_id -= 1
        self.current_id = next_id
        self.time_since_flip = 0

    def update(self, timedelta):
        self.time_since_flip += timedelta
        if self.time_since_flip >= self.durations[self.current_id]:
            self.flip()


class BlinkingAnimation(Animation):
    def __init__(self, image, duration=100):
        super().__init__([image, pygame.Surface(image.get_size(), pygame.SRCALPHA)],
                         duration,
                         is_looping=True)


class StaticAnimation(Animation):
    def __init__(self, image):
        super().__init__([image], 0)

    def update(self, timedelta):
        pass
