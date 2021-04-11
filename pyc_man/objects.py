import pygame
import x_object
from x_animation import *


class Wall(x_object.XObject):
    pass


class Gate(x_object.XObject):
    pass


class Bonus(x_object.XObject):
    def __init__(self, points, *params):
        super().__init__(*params)
        self.points = points


class Pellet(Bonus):
    __sprite_name__ = 'pellet'

    def __init__(self, *params):
        super().__init__(10, *params)

    def get_hit_box(self):
        hit_box = pygame.Rect(0, 0, self.rect.width // 3, self.rect.height // 3)
        hit_box.center = self.rect.center
        return hit_box


class Energizer(Bonus):
    __sprite_name__ = 'energizer'

    def __init__(self, *params):
        super().__init__(50, *params)

    def get_hit_box(self):
        hit_box = pygame.Rect(0, 0, self.rect.width // 2, self.rect.height // 2)
        hit_box.center = self.rect.center
        return hit_box


class Fruits(Bonus, x_object.SpawnableMixin):
    __points__ = [100, 300, 500, 700, 1000, 2000, 3000, 5000]
    __sprite_name__ = 'fruit'

    @classmethod
    def sprite_name(cls, i):
        return cls.__sprite_name__ + '-' + str(i + 1)

    @classmethod
    def count(cls):
        return 8

    __spawnpoint__ = 'fruit'
    __animations__ = {"normal": StaticAnimation, "blinking": BlinkingAnimation}
    __default_state__ = "blinking"

    def __init__(self, *params, **kwargs):
        i = kwargs.get('order', 0)
        super().__init__(self.__points__[i], *params)

        self.animations = dict()
        for state in self.__animations__:
            self.animations[state] = self.__animations__[state](self.image)
        self.state = None
        self.set_state(self.__default_state__)

    def set_state(self, new_state):
        if self.state != new_state:
            self.state = new_state
            self.animation = self.animations[self.state]

    def update(self, timedelta):
        self.image = self.animation.image()
        self.animation.update(timedelta)


    def get_hit_box(self):
        hit_box = pygame.Rect(0, 0, self.rect.width // 2, self.rect.height // 2)
        hit_box.center = self.rect.center
        return hit_box


