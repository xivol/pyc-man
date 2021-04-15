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
        self.actors = None
        self.font = None
        self.score = 0
        self.pellets_count = 0

    def teardown(self):
        self.level.clear_sprites()
        self.pellets_count = 0
        self.level.setup_sprites(self.sprites)
        for actor in self.actors:
            actor.speed *= 1.1
        return super().teardown()

    # def handle_input_event(self, event):
    #     super().handle_input_event(event)
    #
    #     if event.type == pygame.KEYDOWN:
    #         self.done = True
    #
    # def draw(self, surface):
    #     RunningState.draw(self, surface)
    #
    #     level_size_surf = pygame.Surface(self.level.renderer.pixel_size)
    #     text = self.font.render(self.message)
    #     t_w, t_h = text.get_size()
    #     s_w, s_h = self.level.renderer.pixel_size
    #     level_size_surf.blit(text, (s_w // 2 - t_w // 2, s_h // 2 - t_h // 2))
    #
    #     screen_size_surf = pygame.Surface(surface.get_size())
    #     pygame.transform.smoothscale(level_size_surf, surface.get_size(), screen_size_surf)
    #     screen_size_surf.set_colorkey((0, 0, 0))
    #
    #     surface.blit(screen_size_surf, (0, 0))
