from enum import Enum

import pygame

from pyc_man.blinking_animator import BlinkingAnimator
from x_object import XStaticObject, XAnimatedObject
from x_animation import *


class Wall(XStaticObject):
    pass


class Gate(XStaticObject):
    pass


class BonusMixin:
    __points__ = None
    __sound__ = None

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
    __sound__ = 'waka'
    def get_hit_box(self):
        hit_box = pygame.Rect(0, 0, self.rect.width // 3, self.rect.height // 3)
        hit_box.center = self.rect.center
        return hit_box


class XBlinkingObject(XAnimatedObject):
    def __init__(self, image, rect, position=None, *groups):
        super().__init__(BlinkingAnimator(self.__sprite_name__, image, self.__default_state__),
                         position,
                         *groups)


class Energizer(XBlinkingObject, BonusMixin):
    __sprite_name__ = 'energizer'
    __default_state__ = "blinking"
    __points__ = 50
    __sound__ = 'waka'

    def get_hit_box(self):
        hit_box = pygame.Rect(0, 0, self.rect.width // 2, self.rect.height // 2)
        hit_box.center = self.rect.center
        return hit_box


class Fruits(XBlinkingObject, BonusMixin, SpawnableMixin):
    __points__ = [100, 300, 500, 700, 1000, 2000, 3000, 5000]
    __sprite_name__ = 'fruit'
    __default_state__ = "normal"
    __spawnpoint__ = 'fruit'
    __sound__ = 'fruit'

    def get_hit_box(self):
        hit_box = pygame.Rect(0, 0, self.rect.width // 2, self.rect.height // 2)
        hit_box.center = self.rect.center
        return hit_box

    @classmethod
    def types(cls):
        for i, name in enumerate(['Cherry', 'Strawberry', 'Apricot',
                                 'Apple', 'Mellon', 'Galaxian', 'Bell', 'Key']):
            yield type(name, (Fruits,), {
                '__points__': Fruits.__points__[i],
                '__sprite_name__': Fruits.__sprite_name__ + '-' + str(i+1)})
