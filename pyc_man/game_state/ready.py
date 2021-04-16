import pygame
from x_game_state import XGameState


def get(text, color):
    if not text:
        return None, None
    if isinstance(text, str):
        return text, color
    if isinstance(text, tuple):
        return text
    if isinstance(text, dict):
        return text['text'], text['color']
    raise Exception()


def pad(text, width):
    if not text:
        return None
    text = text.strip()
    if len(text) > width:
        return text[:width]
    elif len(text) < width:
        return text.rjust((width + len(text)) // 2)

    return text


class ReadyState(XGameState):
    __title_rect__ = pygame.Rect(9, 14, 10, 1)
    __subtitle_rect__ = pygame.Rect(9, 20, 10, 1)

    def __init__(self, next_state="Running", title=None, subtitle=None, **kwargs):
        super().__init__()
        self.title_text, self.title_color = get(title, kwargs.get('title_color', pygame.Color(0, 255, 255)))
        self.title_text = pad(self.title_text, self.__title_rect__.width)

        self.subtitle_text, self.subtitle_color = get(subtitle, kwargs.get('subtitle_color', pygame.Color(255, 255, 0)))
        self.subtitle_text = pad(self.subtitle_text, self.__subtitle_rect__.width)
        self.next = next_state

        # Persistent values
        self.level = None
        self.font = None

    def handle_input_event(self, event):
        super().handle_input_event(event)

        if event.type == pygame.KEYDOWN:
            self.done = True

    def render(self, text, color, rect, surface):
        if not text:
            return
        img = self.font.render(text, color)
        img.set_colorkey((0, 0, 0))
        surface.blit(img, (rect.x * self.level.tile_width, rect.y * self.level.tile_height))

    def draw(self, surface):
        level_size_surf = pygame.Surface(self.level.renderer.pixel_size)
        self.screen = level_size_surf
        self.level.draw(level_size_surf)
        self.ui.draw(level_size_surf)

        self.render(self.title_text, self.title_color, self.__title_rect__, level_size_surf)
        self.render(self.subtitle_text, self.subtitle_color, self.__subtitle_rect__, level_size_surf)

        pygame.transform.smoothscale(level_size_surf, surface.get_size(), surface)
