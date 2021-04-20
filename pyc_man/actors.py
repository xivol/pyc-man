from abc import ABC, abstractmethod
import pygame
import x_object
from pyc_man import behavior
from pyc_man.behavior import ConsumeHandler, wrap
from x_actor import XActor
from x_animation import Animation, StaticAnimation
from x_input import Direction
from pyc_man.objects import Wall, Gate, SpawnableMixin, BonusMixin
from pyc_man.directional_animator import DirectionalAnimationManager


class Actor(x_object.XAnimatedObject, SpawnableMixin):
    __manager_type__ = DirectionalAnimationManager
    __speed__ = 0

    def __init__(self, *params, **kwargs):
        super().__init__(*params, **kwargs)
        self.speed = self.__speed__
        self.direction = None
        self.makes_turn = False
        self.is_alive = True
        self.sound = None
        self.set_direction(Direction.default())

    def act(self, time, input, game_state):
        self.make_sound(game_state.sounds)

        dist = int(self.speed * time)
        if game_state.level.can_pass(self, self.direction.move(dist)):
            self.make_a_move(dist, game_state.screen.get_size())
        else:
            self.dont_make_a_move(game_state)

        impact = game_state.level.get_hit(self)
        if impact and isinstance(game_state, ConsumeHandler):
            game_state.on_did_consume(self, impact)

    def update(self, time, input, game_state):
        self.act(time, input, game_state)
        self.animate(time)

    def set_direction(self, new_direction):
        if self.direction != new_direction:
            self.makes_turn = True
            self.direction = new_direction
            self.animation.set_direction(new_direction)
        else:
            self.makes_turn = False

    def can_pass(self, object):
        return not isinstance(object, Wall)

    @classmethod
    def can_eat(cls, subject, target):
        return x_object.is_collided(subject, target)

    def make_a_move(self, move_dist, screen):
        move_dist = int(move_dist)
        width, height = screen
        x, y = self.direction.move_point(self.rect.center, move_dist)
        self.rect.center = wrap(x, y, width, height)
        self.makes_turn = False

    def dont_make_a_move(self, game_state):
        pass

    def make_sound(self, sounds, event=None):
        pass

    def get_hit_box(self):
        hit_box = pygame.Rect(0, 0, self.rect.width // 2, self.rect.height // 2)
        hit_box.center = self.rect.center
        return hit_box

    def on_despawn(self, level):
        if self.sound:
            self.sound.stop()


class PacMan(XActor, SpawnableMixin):
    __manager_type__ = DirectionalAnimationManager
    __sprite_name__ = 'pacman'
    __spawnpoint__ = 'pacman'
    __start_lives__ = 2
    __max_lives__ = 5
    __speed__ = 0.16

    __animations__ = {"init": StaticAnimation,
                      "normal": StaticAnimation,
                      "moving": Animation,
                      "dead": Animation}
    __default_state__ = "init"

    def __init__(self, sprite_factory, *params, **kwargs):
        self.extra_lives = self.__start_lives__
        super().__init__(sprite_factory, *params, **kwargs)
        self.makes_turn = False
        self.sound = None
        self.direction = None
        self.set_direction(Direction.default())

    @property
    def is_alive(self):
        return isinstance(self.state, behavior.DyingPacMan)

    def set_direction(self, new_direction):
        if self.direction != new_direction:
            self.makes_turn = True
            self.direction = new_direction
            self.animation.set_direction(new_direction)
        else:
            self.makes_turn = False

    @classmethod
    def can_eat(cls, subject, target):
        return x_object.is_collided(subject, target)

    def get_hit_box(self):
        hit_box = pygame.Rect(0, 0, self.rect.width // 2, self.rect.height // 2)
        hit_box.center = self.rect.center
        return hit_box

    def die(self):
        self.state.next = 'dying'
        self.state.done = True

    def revive(self):
        self.extra_lives -= 1
        self.state.next = 'init'
        self.state.done = True


class Ghost(Actor):
    __sprite_name__ = 'ghost'
    __spawnpoint__ = 'ghost-4'
    __speed__ = 0.1

    __animations__ = {'normal': Animation,
                      'dead': Animation,
                      'frighten-normal': Animation,
                      'frighten-timeout': Animation}
    __default_state__ = "normal"

    __sound__ = 'ghost'

    def act(self, time, input, game_state):
        if game_state.screen:
            self.set_direction(self.direction)
            super().act(time, input, game_state)

    def dont_make_a_move(self, game_state):
        d = Direction((self.direction.value + 1) % 4)
        self.set_direction(Direction.random())

    @property
    def behavior(self):
        return self

    @classmethod
    def can_eat(cls, subject, target):
        if isinstance(target, PacMan):
            return x_object.is_collided(subject, target)
        return 0

    def make_sound(self, sounds, event=None):
        if sounds[self.__sound__].get_num_channels() < 1:
            self.sound = sounds[self.__sound__].play()
