import enum
import random

import pygame


class Direction(enum.Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    def __str__(self):
        return self.name.lower()
    @staticmethod
    def all():
        return [Direction.LEFT, Direction.RIGHT, Direction.UP, Direction.DOWN]

    @staticmethod
    def default():
        return Direction.RIGHT

    @staticmethod
    def random():
        return random.choice(Direction.all())

    def move(self, delta):
        return self.move_point((0,0), delta)

    def move_point(self, point, delta):
        if self == Direction.UP:
            return (point[0], point[1] - delta)
        if self == Direction.RIGHT:
            return (point[0] + delta, point[1])
        if self == Direction.DOWN:
            return (point[0], point[1] + delta)
        if self == Direction.LEFT:
            return (point[0]-delta, point[1])


class XGameInput(object):
    def __init__(self):
        self.keys_pressed=set()

    def key_down(self, event):
        if event.type != pygame.KEYDOWN:
            raise Exception()
        self.keys_pressed.add(event.key)

    def key_up(self, event):
        if event.type != pygame.KEYUP:
            raise Exception()
        self.keys_pressed.remove(event.key)