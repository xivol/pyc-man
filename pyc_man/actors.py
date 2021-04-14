from abc import ABC, abstractmethod
import pygame

import x_object
from x_animation import Animation
from x_input import Direction
from pyc_man.objects import Wall, Gate, SpawnableMixin
from pyc_man.directional_animator import DirectionalAnimationManager



def wrap(x, y, width, height):
    if not 0 <= x < width:
        x = (x + width) % width
    if not 0 <= y < height:
        y = (y + height) % height
    return x, y


class ConsumeHandler:
    @abstractmethod
    def on_did_consume(self, subject, target):
        pass


class Actor(x_object.XAnimatedObject, SpawnableMixin, ABC):
    __manager_type__ = DirectionalAnimationManager
    __speed__ = 0

    def __init__(self, *params, **kwargs):
        self.speed = self.__speed__
        self.direction = None
        self.makes_turn = False
        self.set_direction(Direction.default())
        super().__init__(*params, **kwargs)

    @abstractmethod
    def act(self, time, input, game_state):
        pass

    def update(self, time, input, game_state):
        self.act(time, input, game_state)
        self.animate(time)

    def set_direction(self, new_direction):
        if self.direction != new_direction:
            self.makes_turn = True
            self.direction = new_direction
            return True
        else:
            self.makes_turn = False

    def can_pass(self, object):
        return not isinstance(object, Wall)

    def make_a_move(self, move_dist, screen):
        width, height = screen
        x, y = self.direction.move_point(self.rect.center, move_dist)
        self.rect.center = wrap(x, y, width, height)

    def get_hit_box(self):
        hit_box = pygame.Rect(0, 0, self.rect.width // 2, self.rect.height // 2)
        hit_box.center = self.rect.center
        return hit_box


class PacMan(Actor):
    __sprite_name__ = 'pacman'
    __spawnpoint__ = 'pacman'
    __start_lives__ = 3
    __max_lives__ = 5
    __speed__ = 0.2

    __animations__ = {"normal": Animation, "dead": Animation}
    __default_state__ = "normal"

    def __init__(self, sprite_factory, *params, **kwargs):
        self.lives = self.__start_lives__
        self.is_alive = True
        super().__init__(sprite_factory, *params, **kwargs)

    def act(self, time, input, game_state):
        if not self.is_alive:
            return

        if input.direction:
            if self.set_direction(input.direction):
                self.animation.set_direction(input.direction)
            if game_state.level.can_pass(self, self.direction.move(self.speed * time)):
                self.make_a_move(self.speed * time, game_state.screen.get_size())

        impact = self.get_hit(game_state.level.collider_sprites)
        if impact and isinstance(game_state, ConsumeHandler):
            game_state.on_did_consume(self, impact)

    def can_pass(self, object):
        return not (isinstance(object, Wall) or isinstance(object, Gate))

    def die(self):
        self.lives -= 1
        self.is_alive = False


class Ghost(Actor):
    __spawnpoint__ = 'ghost'
    __speed__ = 0.18

    def act(self, time, input, game_state):
        pass