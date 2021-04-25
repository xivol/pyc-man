from abc import abstractmethod
from enum import Enum

import x_actor
from x_input import Direction
from pyc_man.objects import Wall, Gate, BonusMixin, Fruits
from x_sound import XSoundMixin


class ConsumeHandler:
    @abstractmethod
    def on_did_consume(self, subject, target):
        pass


class Moving(x_actor.XBehavior):
    def __init__(self, speed, animation, persists=set()):
        super().__init__(animation, persists=persists | {'speed'})
        self.speed = speed

    def enact(self, actor, timedelta, world):
        dist = int(self.speed * timedelta)
        if world.level.can_pass(actor, actor.direction.move(dist)):
            self.make_a_move(actor, dist, world.level)
        else:
            self.dont_make_a_move(actor, world)

        target = world.level.get_hit(actor)
        if self.can_eat(target) and isinstance(world, ConsumeHandler):
            # actor.make_sound(world.sounds, target.__sound__)
            self.make_a_sound(actor, target, world.sounds)
            world.on_did_consume(actor, target)

    def can_pass(self, object):
        return not isinstance(object, Wall)

    def can_eat(self, object):
        return False

    def make_a_move(self, actor, move_dist, level):
        move_dist = int(move_dist)
        x, y = actor.direction.move_point(actor.rect.center, move_dist)
        actor.rect.center = level.wrap(x, y)
        actor.makes_turn = False

    def dont_make_a_move(self, actor, world):
        pass

    def make_a_sound(self, actor, event, sounds):
        pass

    def dont_make_a_sound(self, actor, sounds):
        pass


class NormalPacMan(x_actor.XBehavior):
    def handle_input(self, actor, timedelta, input, world_state):
        if input.direction:
            actor.change_behavior(actor.Behavior.MOVE)


class DyingPacMan(x_actor.XBehavior):
    pass


class MovingPacMan(Moving):
    class Sound(Enum):
        EAT_FRUIT = 'fruit'
        EAT_GHOST = 'ghost'
        EAT = 'waka'

    def handle_input(self, actor, timedelta, input, world_state):
        if not input.direction:
            actor.change_behavior(actor.Behavior.STILL)
        else:
            actor.set_direction(input.direction)

    def can_pass(self, object):
        return not isinstance(object, Wall) and \
               not isinstance(object, Gate)

    def can_eat(self, object):
        return isinstance(object, BonusMixin) or \
               (isinstance(object, x_actor.XActor) and
                isinstance(object.behavior, FrightGhost))

    def make_a_move(self, actor, move_dist, screen):
        actor.animation.set_state(self.animation)
        super().make_a_move(actor, move_dist, screen)

    def dont_make_a_move(self, actor, world):
        self.dont_make_a_sound(actor, world.sounds)
        actor.change_behavior(actor.Behavior.STILL)

    def make_a_sound(self, actor, event, sounds):
        if isinstance(actor, XSoundMixin):
            if isinstance(event, x_actor.XActor):
                actor.play_sound(self.Sound.EAT_GHOST, sounds.effects)
            elif isinstance(event, Fruits):
                actor.play_sound(self.Sound.EAT_FRUIT, sounds.effects)
            else:
                actor.play_sound(self.Sound.EAT, sounds.pacman)

    def dont_make_a_sound(self, actor, sounds):
        actor.stop_sound(sounds.pacman)


class ChaseGhost(Moving):
    def dont_make_a_move(self, actor, world):
        actor.set_direction(Direction.random())

    def can_eat(self, object):
        return isinstance(object, x_actor.XActor) and \
               (isinstance(object.behavior, NormalPacMan) or \
                isinstance(object.behavior, MovingPacMan))


class FrightGhost(Moving):
    def dont_make_a_move(self, actor, world):
        actor.set_direction(Direction.random())

    def enter(self, actor):
        super().enter(actor)
        actor.set_direction(Direction.opposite(actor.direction))

class FlickerGhost(FrightGhost):
    pass

class DeadGhost(Moving):
    pass
