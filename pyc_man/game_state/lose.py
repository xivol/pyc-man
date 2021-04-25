import pygame
from pyc_man.actors import PacMan
from pyc_man.behaviors import DyingPacMan
from .running import RunningState
from pyc_man.game_state.ready import ReadyState


class LoseState(ReadyState):
    __music_on_startup__ = 'death'

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
        pygame.time.wait(500)
        super().setup(**persist_values)
        if self.title in self.ui:
            self.ui.remove(self.title)
        if self.subtitle in self.ui:
            self.ui.remove(self.subtitle)

        for actor in self.actors:
            if isinstance(actor, PacMan):
                self.pacman = actor
                actor.change_behavior(PacMan.Behavior.DEAD)
                actor.flip_state()
            else:
                self.level.remove(actor)

    def update(self, timedelta):
        self.pacman.animate(timedelta)
        if self.pacman.animation.current().is_finished():
            if self.title:
                self.ui.add(self.title)
            if self.subtitle:
                self.ui.add(self.subtitle)

        self.dirty = True
