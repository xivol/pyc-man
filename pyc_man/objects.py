import pygame
from x_object import XStaticObject, XAnimatedObject
from x_animation import *


class Wall(XStaticObject):
    pass


class Gate(XStaticObject):
    pass


class BonusMixin:
    __points__ = None
    @classmethod
    def points(cls):
        return cls.__points__


class SpawnableMixin:
    __spawnpoint__ = None

    @classmethod
    def spawnpoint(cls):
        return cls.__spawnpoint__


class Pellet(XStaticObject, BonusMixin):
    __sprite_name__ = 'pellet'
    __points__ = 10

    def get_hit_box(self):
        hit_box = pygame.Rect(0, 0, self.rect.width // 3, self.rect.height // 3)
        hit_box.center = self.rect.center
        return hit_box


class Energizer(XStaticObject, BonusMixin):
    __sprite_name__ = 'energizer'
    __points__ = 50

    def get_hit_box(self):
        hit_box = pygame.Rect(0, 0, self.rect.width // 2, self.rect.height // 2)
        hit_box.center = self.rect.center
        return hit_box


class Fruits(XAnimatedObject, BonusMixin, SpawnableMixin):
    __points__ = [100, 300, 500, 700, 1000, 2000, 3000, 5000]
    __sprite_name__ = 'fruit'

    @classmethod
    def points(cls, i):
        return cls.__points__[i]

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
        super().__init__()
        self.animator = AnimationManager(self.__sprite_name__,
                                         self.__sprite_factory__(),
                                         self.__animations__,
                                         self.__default_state__)

    def update(self, timedelta):
        self.image = self.animator.current().image()
        self.animator.update(timedelta)

    def get_hit_box(self):
        hit_box = pygame.Rect(0, 0, self.rect.width // 2, self.rect.height // 2)
        hit_box.center = self.rect.center
        return hit_box


