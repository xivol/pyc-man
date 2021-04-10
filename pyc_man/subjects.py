from abc import ABC
import pygame
import enum

import x_subject
import x_object
from pyc_man.game_state.basic import BasicState
from pyc_man.objects import Wall, Gate


class Actor(x_subject.XSubject, x_object.SpawnableMixin, ABC):
    __speed__ = 0

    def __init__(self, *params):
        super().__init__(*params)
        self.direction = None
        self.set_direction(Direction.RIGHT)
        self.speed = self.__speed__
        self.is_alive = True

    def set_direction(self, direction):
        if self.direction != direction:
            self.makes_turn = True
            self.direction = direction
        else:
            self.makes_turn = False

    def can_pass(self, object):
        return not isinstance(object, Wall)

    def get_hit_box(self):
        hit_box = pygame.Rect(0, 0, self.rect.width//2, self.rect.height//2)
        hit_box.center = self.rect.center
        return hit_box


class PacMan(Actor):
    __spawnpoint__ = 'pacman'
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
            if game_state.game.level.can_pass(self, self.direction.move(self.speed * time)):
                self.make_a_move(self.speed * time, game_state.screen.get_size())

        impact = self.get_hit(game_state.game.level.collider_sprites)
        if impact and isinstance(game_state, BasicState):
            game_state.on_did_consume(self, impact)

    def can_pass(self, object):
        return not (isinstance(object, Wall) or isinstance(object, Gate))

    def make_a_move(self, move_dist, screen):
        width, height = screen
        x, y = center = self.direction.move_point(self.rect.center, move_dist)
        if not 0 < x < width:
            center = ((x + width) % width, y)
        self.rect.center = center

    def die(self):
        self.lives -= 1
        self.is_alive = False


class Ghost(Actor):
    __spawnpoint__ = 'ghost'
    __speed__ = 0.2



