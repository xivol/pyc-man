import pygame

from pyc_man.objects import Bonus
from pyc_man.subjects import PacMan, Direction
from pyc_man.game_state.basic import BasicState


class RunningState(BasicState):
    def handle_input_event(self, event):
        super().handle_input_event(event)

        if event.type == pygame.KEYUP:
            self.input.direction = None

        if self.input.keys_pressed:
            if pygame.K_UP in self.input.keys_pressed:
                self.input.direction = Direction.UP
            elif pygame.K_DOWN in self.input.keys_pressed:
                self.input.direction = Direction.DOWN
            elif pygame.K_RIGHT in self.input.keys_pressed:
                self.input.direction = Direction.RIGHT
            elif pygame.K_LEFT in self.input.keys_pressed:
                self.input.direction = Direction.LEFT

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.input.direction = Direction.UP
            elif event.key == pygame.K_DOWN:
                self.input.direction = Direction.DOWN
            elif event.key == pygame.K_RIGHT:
                self.input.direction = Direction.RIGHT
            elif event.key == pygame.K_LEFT:
                self.input.direction = Direction.LEFT

    def on_did_consume(self, subject, target):
        if isinstance(subject, PacMan) and isinstance(target, Bonus):
            subject.points += target.points
            self.game.set_score(subject.points)
            self.game.level.remove(target)

class ChaseState(RunningState):
    pass


class FrightState(RunningState):
    pass
