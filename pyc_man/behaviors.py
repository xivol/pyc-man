from abc import abstractmethod

import x_actor
from x_input import Direction
from pyc_man.actors import PacMan, Ghost
from pyc_man.objects import Wall, Gate, BonusMixin


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


class NormalPacMan(x_actor.XBehavior):
    def handle_input(self, actor, timedelta, input, world_state):
        if input.direction:
            self.done = True
            self.next = "moving"


class DyingPacMan(x_actor.XBehavior):
    def __init__(self, animation, sound):
        super().__init__(animation)
        self.sound = sound


class MovingPacMan(Moving):
    def handle_input(self, actor, timedelta, input, world_state):
        if not input.direction:
            self.done = True
            self.next = "normal"
        else:
            actor.set_direction(input.direction)

    def can_pass(self, object):
        return not isinstance(object, Wall) and \
               not isinstance(object, Gate)

    def can_eat(self, object):
        return isinstance(object, BonusMixin) or \
               (isinstance(object, Ghost) and
                isinstance(object.behavior, FrightGhost))

    def make_a_move(self, actor, move_dist, screen):
        actor.animation.set_state(self.animation)
        super().make_a_move(actor, move_dist, screen)

    def dont_make_a_move(self, actor, world):
        self.done = True
        self.next = "normal"


class ChaseGhost(Moving):
    def dont_make_a_move(self, actor, world):
        actor.set_direction(Direction.random())

    def can_eat(self, object):
        return isinstance(object, PacMan)


class FrightGhost(Moving):
    def __init__(self, animation):
        super().__init__(0, animation)
        self.timeout = False

    def dont_make_a_move(self, actor, world):
        actor.set_direction(Direction.random())

    def enter(self, actor):
        super().enter(actor)
        actor.set_direction(Direction.opposite(actor.direction))
        self.timeout = False

    def start_timeout(self):
        self.timeout = True

    def enact(self, actor, timedelta, world):
        if self.timeout:
            actor.animation.set_state('frighten-timeout')
        super().enact(actor, timedelta, world)


class DeadGhost(Moving):
    pass
