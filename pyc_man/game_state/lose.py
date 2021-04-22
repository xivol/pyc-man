import pygame
from pyc_man.actors import PacMan
from .running import RunningState
from pyc_man.game_state.ready import ReadyState


class LoseState(ReadyState):
    __on_startup__ = 'death'

    def __init__(self, message, message_color, next_state):
        super().__init__(next_state, subtitle=message, subtitle_color=message_color)

        # Persistent values
        # just to silence warnings
        self.level = None
        self.sprites = None
        self.actors = None

        self.pacman = None

    def handle_input_event(self, event):
        super().handle_input_event(event)
        if not self.pacman.animation.current().is_finished():
            self.done = False

    def setup(self, **persist_values):
        super().setup(**persist_values)
        for actor in self.actors:
            if isinstance(actor, PacMan):
                self.pacman = actor
            else:
                self.level.remove(actor)

    def update(self, timedelta):
        if not self.pacman.animation.current().is_finished():
            self.level.update(timedelta, self.input, self)
            self.dirty = True

    def draw(self, surface):
        if not self.pacman.animation.current().is_finished():
            RunningState.draw(self, surface)
        else:
            super().draw(surface)