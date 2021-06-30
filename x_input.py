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
    def opposite(direction):
        return Direction((direction.value + 2) % 4)

    @staticmethod
    def random():
        return random.choice(Direction.all())

    @staticmethod
    def calc(from_point, to_point):
        if from_point == to_point:
            raise ValueError(from_point, to_point)

        dx = to_point[0] - from_point[0]
        dy = to_point[1] - from_point[1]
        if abs(dx) > abs(dy):
            if dx < 0:
                return Direction.LEFT
            else:
                return Direction.RIGHT
        elif abs(dx) < abs(dy):
            if dy < 0:
                return Direction.DOWN
            else:
                return Direction.UP
        else:
            if dy < 0:
                if dx < 0:
                    return random.choice([Direction.DOWN, Direction.LEFT])
                else:
                    return random.choice([Direction.DOWN, Direction.RIGHT])
            else:
                if dx < 0:
                    return random.choice([Direction.UP, Direction.LEFT])
                else:
                    return random.choice([Direction.UP, Direction.RIGHT])

    def move(self, delta):
        return self.move_point((0, 0), delta)

    def move_point(self, point, delta):
        if self == Direction.UP:
            return (point[0], point[1] - delta)
        if self == Direction.RIGHT:
            return (point[0] + delta, point[1])
        if self == Direction.DOWN:
            return (point[0], point[1] + delta)
        if self == Direction.LEFT:
            return (point[0] - delta, point[1])


class XGameInput(object):
    def __init__(self):
        self.keys_pressed = set()

    def key_down(self, event):
        if event.type != pygame.KEYDOWN:
            raise Exception()
        self.keys_pressed.add(event.key)

    def key_up(self, event):
        if event.type != pygame.KEYUP:
            raise Exception()
        self.keys_pressed.remove(event.key)
