import pygame

from pyc_man.game_state import RunningState
from x_game_state import XGameState


class WinState(XGameState):
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
        self.score = 0
        self.pellets_count = 0
        self.current_bonus = 0

    def teardown(self):
        self.level.clear_sprites()
        self.pellets_count = 0
        return super().teardown()

    def handle_input_event(self, event):
        super().handle_input_event(event)

        if event.type == pygame.KEYDOWN:
            self.next = "Running"
            self.done = True

    def draw(self, surface):
        RunningState.draw(self, surface)

        level_screen = pygame.Surface(self.level.renderer.pixel_size)
        text = self.font.render(self.message)
        t_w, t_h = text.get_size()
        s_w, s_h = level_screen.get_size()
        level_screen.blit(text, (s_w // 2 - t_w // 2, s_h // 2 - t_h // 2))

        temp = pygame.Surface(surface.get_size())
        pygame.transform.smoothscale(level_screen, surface.get_size(), temp)
        temp.set_colorkey((0, 0, 0))
        surface.blit(temp, (0, 0))
