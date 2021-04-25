import pygame
from enum import Enum

from x_actor import XActor
from x_animation import Animation, StaticAnimation
from x_input import Direction
from pyc_man import behaviors
from pyc_man.objects import SpawnableMixin
from pyc_man.directional_animator import DirectionalAnimationManager


class PMActor(XActor, SpawnableMixin):
    __manager_type__ = DirectionalAnimationManager
    __speed__ = 0

    def __init__(self, *params, **kwargs):
        super().__init__(*params, **kwargs)
        self.direction = None
        self.makes_turn = False
        self.set_direction(Direction.default())

    def set_direction(self, new_direction):
        if self.direction != new_direction:
            self.makes_turn = True
            self.direction = new_direction
            self.animation.set_direction(new_direction)
        else:
            self.makes_turn = False

    @property
    def is_alive(self):
        return True

    def get_hit_box(self):
        hit_box = pygame.Rect(0, 0, self.rect.width // 2, self.rect.height // 2)
        hit_box.center = self.rect.center
        return hit_box


class PacMan(PMActor):
    __sprite_name__ = 'pacman'
    __spawnpoint__ = 'pacman'
    __start_lives__ = 2
    __max_lives__ = 5
    __speed__ = 0.16

    __animations__ = {"init": StaticAnimation,
                      "normal": StaticAnimation,
                      "moving": Animation,
                      "dead": Animation}
    __default_anim__ = "init"

    class Behavior(Enum):
        ROUND = 'init'
        STILL = 'normal'
        MOVE = 'moving'
        DEAD = 'dead'

    __behaviors__ = {
        Behavior.ROUND: behaviors.NormalPacMan('init'),
        Behavior.STILL: behaviors.NormalPacMan('normal'),
        Behavior.MOVE: behaviors.MovingPacMan(__speed__, 'moving'),
        Behavior.DEAD: behaviors.DyingPacMan('dead')
    }

    __default_behavior__ = Behavior.ROUND

    __sounds__ = {
        behaviors.MovingPacMan.Sound.EAT_FRUIT: 'pacman_eat_fruit',
        behaviors.MovingPacMan.Sound.EAT_GHOST: 'pacman_eat_ghost',
        behaviors.MovingPacMan.Sound.EAT: 'pacman_eat_waka'
    }

    def __init__(self, *params, **kwargs):
        super().__init__( *params, **kwargs)
        self.extra_lives = self.__start_lives__

    @property
    def is_alive(self):
        return not isinstance(self.state, behaviors.DyingPacMan)

    def revive(self):
        self.extra_lives -= 1
        self.change_behavior(PacMan.Behavior.ROUND)


class Ghost(PMActor):
    __sprite_name__ = 'ghost'
    __spawnpoint__ = 'ghost-4'
    __speed__ = 0.1
    __points__ = 200

    @staticmethod
    def points():
        return Ghost.__points__

    __animations__ = {'normal': Animation,
                      'dead': Animation,
                      'frighten-normal': Animation,
                      'frighten-timeout': Animation}
    __default_anim__ = "normal"

    class Behavior(Enum):
        CHASE = 'chase'
        FRIGHT = 'fright'
        FLICKER = 'flicker'
        DEAD = 'dead'

    __behaviors__ = {
        Behavior.CHASE: behaviors.ChaseGhost(__speed__, 'normal'),
        Behavior.FRIGHT: behaviors.FrightGhost(__speed__, 'frighten-normal'),
        Behavior.FLICKER: behaviors.FlickerGhost(__speed__, 'frighten-timeout'),
        Behavior.DEAD: behaviors.DeadGhost(__speed__, 'dead')
    }

    __default_behavior__ = Behavior.CHASE
