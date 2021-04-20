from abc import abstractmethod, ABC
import x_actor

from pyc_man.objects import Wall, Gate, BonusMixin


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


class Moving(x_actor.XBehavior):
    def __init__(self, speed, animation):
        super().__init__(animation, persists={'speed'})
        self.speed = speed

    def enact(self, actor, timedelta, world):
        dist = int(self.speed * timedelta)
        if world.level.can_pass(actor, actor.direction.move(dist)):
            self.make_a_move(actor, dist, world.screen.get_size())
        else:
            self.dont_make_a_move(actor, world)

        impact = world.level.get_hit(actor)
        if impact and isinstance(world, ConsumeHandler):
            world.on_did_consume(actor, impact)

    def can_pass(self, object):
        return not isinstance(object, Wall)

    def make_a_move(self, actor, move_dist, screen):
        move_dist = int(move_dist)
        width, height = screen
        x, y = actor.direction.move_point(actor.rect.center, move_dist)
        actor.rect.center = wrap(x, y, width, height)
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

    def enact(self, actor, timedelta, world):
        actor.make_sound(world.sounds, self.sound)

class MovingPacMan(Moving):
    def handle_input(self, actor, timedelta, input, world_state):
        if not input.direction:
            self.done = True
            self.next = "normal"
        else:
            actor.set_direction(input.direction)

    def can_pass(self, object):
        return not isinstance(object, Wall) and not isinstance(object, Gate)

    def make_a_move(self, actor, move_dist, screen):
        actor.animation.set_state(self.animation)
        super().make_a_move(actor, move_dist, screen)

    def dont_make_a_move(self, actor, world):
        self.done = True
        self.next = "normal"


class ChaseGhost(Moving):
    def enact(self, actor, timedelta, world_state):
        pass


class FrightGhost(Moving):
    def enact(self, actor, timedelta, world_state):
        pass


class DeadGhost(Moving):
    def enact(self, actor, timedelta, world_state):
        pass

