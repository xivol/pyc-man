import pygame
import x_object
from pyc_man import behaviors
from x_actor import XActor
from x_animation import Animation, StaticAnimation
from x_input import Direction
from pyc_man.objects import Wall, Gate, SpawnableMixin, BonusMixin
from pyc_man.directional_animator import DirectionalAnimationManager


class PMActor(XActor, SpawnableMixin):
    __manager_type__ = DirectionalAnimationManager
    __speed__ = 0

    def __init__(self, *params, **kwargs):
        super().__init__(*params, **kwargs)
        self.direction = None
        self.makes_turn = False
        self.sound = None
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

    def on_despawn(self, level):
        if self.sound:
            self.sound.stop()


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
        return not isinstance(self.state, behaviors.DyingPacMan)

    def die(self):
        self.state.next = 'dying'
        self.state.done = True

    def revive(self):
        self.extra_lives -= 1
        self.state.next = 'init'
        self.state.done = True


class Ghost(PMActor):
    __sprite_name__ = 'ghost'
    __spawnpoint__ = 'ghost-4'
    __speed__ = 0.1

    __animations__ = {'normal': Animation,
                      'dead': Animation,
                      'frighten-normal': Animation,
                      'frighten-timeout': Animation}
    __default_state__ = "normal"

    __sound__ = 'ghost'
