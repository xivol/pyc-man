from abc import abstractmethod
from enum import Enum

import x_actor
from pyc_man.target_provider import TargetProvider
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
        return not isinstance(object, Wall) and \
               not isinstance(object, Gate)

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


class MovingGhost(Moving):
    __dist__ = min
    def __init__(self, speed, animation, persists=set()):
        super().__init__(speed, animation, persists=persists | {'target_prov'})
        self.target_prov = TargetProvider()

    def handle_input(self, actor, timedelta, input, world):
        if world.level.at_crossing(actor):
            actor.set_direction(self.find_direction(actor, world))

    def dont_make_a_move(self, actor, world):
        actor.set_direction(self.find_direction(actor, world))

    def find_direction(self, actor, world):
        if self.target_prov is None:
            return Direction.random()

        step = world.level.tile_width
        possible_dirs = Direction.all()
        possible_dirs.remove(Direction.opposite(actor.direction))
        possible_dirs = list(filter(lambda d:
                                    world.level.can_pass(actor, d.move(step)),
                                    possible_dirs))
        if len(possible_dirs) == 0:
            return actor.direction

        pos = actor.rect.center
        target = self.target_prov.get_target(world)

        dist_to_target = [world.level.distance(target,
                                               d.move_point(pos, step))
                          for d in possible_dirs]
        index, _ = self.__dist__(enumerate(dist_to_target), key=lambda p: p[1])

        return possible_dirs[index]


class ChaseGhost(MovingGhost):
    def can_eat(self, object):
        return isinstance(object, x_actor.XActor) and \
               (isinstance(object.behavior, NormalPacMan) or \
                isinstance(object.behavior, MovingPacMan))


class FrightGhost(MovingGhost):
    __dist__ = max

    def enter(self, actor):
        super().enter(actor)
        actor.set_direction(Direction.opposite(actor.direction))


class FlickerGhost(FrightGhost):
    pass


class DeadGhost(MovingGhost):
    pass
