import pygame

from pyc_man.actors import PacMan
from pyc_man.game_state import RunningState
from x_game_state import XGameState


class LoseState(XGameState):
    def __init__(self, message):
        super().__init__()
        self.input.direction = None
        self.message = message

        # Persistent values
        self.level = None
        self.sprites = None
        self.actors = None
        self.font = None
        self.bonuses = None

        self.pacman = None

    def setup(self, **persist_values):
        super().setup(**persist_values)
        for actor in self.actors:
            if isinstance(actor, PacMan):
                self.pacman=actor
                self.pacman.die()
            else:
                self.level.remove(actor)

    def handle_input_event(self, event):
        super().handle_input_event(event)

        if self.pacman.animation.current().is_finished() and\
                event.type == pygame.KEYDOWN:
            self.next = "Running"
            self.done = True

    def update(self, timedelta):
        if not self.pacman.animation.current().is_finished():
            self.level.update(timedelta, self.input, self)
            self.dirty = True

    def draw(self, surface):
        RunningState.draw(self, surface)

        if self.pacman.animation.current().is_finished():
            level_size_surf = pygame.Surface(self.level.renderer.pixel_size)
            text = self.font.render(self.message)
            t_w, t_h = text.get_size()
            s_w, s_h = self.level.renderer.pixel_size
            level_size_surf.blit(text, (s_w // 2 - t_w // 2, s_h // 2 - t_h // 2))

            screen_size_surf = pygame.Surface(surface.get_size())
            pygame.transform.smoothscale(level_size_surf, surface.get_size(), screen_size_surf)
            screen_size_surf.set_colorkey((0, 0, 0))

            surface.blit(screen_size_surf, (0, 0))