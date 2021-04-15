import pygame
from pyc_man.actors import PacMan
from pyc_man.game_state import RunningState
from pyc_man.game_state.ready import ReadyState


class LoseState(ReadyState):
    def __init__(self, message="uh-oh!", message_color=pygame.Color(255, 184, 81)):
        super().__init__(subtitle=message, subtitle_color=message_color)

        # Persistent values
        # just to silence warnings
        self.level = None
        self.sprites = None
        self.actors = None

        self.pacman = None

    def setup(self, **persist_values):
        super().setup(**persist_values)
        for actor in self.actors:
            if isinstance(actor, PacMan):
                self.pacman = actor
                self.pacman.die()
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