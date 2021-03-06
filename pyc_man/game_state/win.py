import pygame

from pyc_man.actors import PacMan
from .running import RunningState
from pyc_man.game_state.ready import ReadyState


class WinState(ReadyState):
    __music_on_startup__ = "intermission"

    def __init__(self, message, next_state):
        if len(message) > 10:
            title = message[:10].strip()
            subtitle = message[10:].strip()
        else:
            title = message
            subtitle = None

        super().__init__(next_state, title=title, subtitle=subtitle)
        self.input.direction = None

        # Persistent values
        self.level = None
        self.sprites = None
        self.actors = None
        self.pellets_count = 0

    def setup(self, **persist_values):
        pygame.time.wait(500)
        super().setup(**persist_values)
        self.level.set_blinking(True)
        for actor in self.actors:
            if not isinstance(actor, PacMan):
                self.level.remove(actor)

    def teardown(self):
        self.level.clear_sprites()
        self.pellets_count = 0
        self.level.setup_sprites(self.sprites)
        self.level.set_blinking(False)
        for actor in self.actors:
            actor.behavior.speed *= 1.1
        return super().teardown()

    def update(self, timedelta):
        self.level.blink(timedelta)
        self.dirty = True
