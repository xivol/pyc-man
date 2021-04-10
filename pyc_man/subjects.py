from abc import ABC

import pygame

import x_subject
import enum

from pyc_man.objects import Wall


class Direction(enum.Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    def move(self, point, delta):
        if self == Direction.UP:
            return (point[0], point[1] - delta)
        if self == Direction.RIGHT:
            return (point[0] + delta, point[1])
        if self == Direction.DOWN:
            return (point[0], point[1] + delta)
        if self == Direction.LEFT:
            return (point[0]-delta, point[1])


class Actor(x_subject.XSubject, ABC):
    __speed__ = 0

    def __init__(self, *params):
        super().__init__(*params)
        self.direction = None
        self.set_direction(Direction.RIGHT)
        self.speed = self.__speed__
        self.is_alive = True

    def set_direction(self, direction):
        if self.direction != direction:
            self.direction = direction


class PacMan(Actor):
    __max_lives__ = 5
    __speed__ = 0.2

    def __init__(self, *params):
        super().__init__(*params)
        self.lives = self.__max_lives__
        self.points = 0

    def act(self, time, input, game_state):
        if not self.is_alive:
            return

        if input.direction:
            self.set_direction(input.direction)
            if not game_state.game.has_wall(self.rect.center, self.direction):
                self.make_a_move(self.speed * time, game_state.screen.get_size())

        if input.impact:
            print(input.impact)

    def get_hit_box(self):
        hit_box = pygame.Rect(0, 0, self.rect.width//2, self.rect.height//2)
        hit_box.center = self.rect.center
        return hit_box

    def make_a_move(self, move_dist, screen):
        width, height = screen
        x, y = center = self.direction.move(self.rect.center, move_dist)
        if not 0 < x < width:
            center = ((x + width) % width, y)
        self.rect.center = center

    def dies(self):
        self.lives -= 1
        self.is_alive = False


