import pygame

from pyc_man.game_state import RunningState
from pyc_man.game_state.ready import ReadyState
from x_game_state import XGameState


class WinState(ReadyState):
    def __init__(self, message):
        if len(message) > 10:
            title = message[:10].strip()
            subtitle = message[10:].strip()
        else:
            title = message
            subtitle = None

        super().__init__(title=title, subtitle=subtitle)
        self.input.direction = None

        # Persistent values
        self.level = None
        self.sprites = None
        self.actors = None
        self.pellets_count = 0

    def teardown(self):
        self.level.clear_sprites()
        self.pellets_count = 0
        self.level.setup_sprites(self.sprites)
        for actor in self.actors:
            actor.speed *= 1.1
        return super().teardown()