import pygame
from x_game_state import XGameState
from pyc_man.ui import UIText


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
    __music_on_startup__ = 'ready'

    def __init__(self, next_state, title=None, subtitle=None, **kwargs):
        super().__init__(next_state)
        self.title_text, self.title_color = get(title, kwargs.get('title_color', pygame.Color(0, 255, 255)))
        self.title_text = pad(self.title_text, self.__title_rect__.width)

        self.subtitle_text, self.subtitle_color = get(subtitle, kwargs.get('subtitle_color', pygame.Color(255, 255, 0)))
        self.subtitle_text = pad(self.subtitle_text, self.__subtitle_rect__.width)

        # Persistent values
        self.level = None
        self.actors = None
        self.font = None
        self.ui = None
        self.sounds = None
        self.fruit = None

        self.title = None
        self.subtitle = None

    def setup(self, **persist_values):
        super().setup(**persist_values)

        if self.__music_on_startup__:
            self.music = self.sounds.music.play(self.__music_on_startup__, fade_ms=100)

        self.title = self.make_text(self.title_text, self.title_color, 'left', self.__title_rect__)
        if self.title:
            self.ui.add(self.title)
        self.subtitle = self.make_text(self.subtitle_text, self.subtitle_color, 'left', self.__subtitle_rect__)
        if self.subtitle:
            self.ui.add(self.subtitle)

        if self.fruit:
            self.level.remove(self.fruit)
            self.fruit = None

    def teardown(self):
        self.sounds.music.fadeout(100)

        for actor in self.actors:
            if not actor.is_alive:
                actor.revive()
            self.level.spawn(actor)

        self.ui.remove(self.title)
        self.ui.remove(self.subtitle)

        self.input.direction = None
        return super().teardown()

    def handle_input_event(self, event):
        super().handle_input_event(event)

        if event.type == pygame.KEYDOWN:
            self.done = True

    def make_text(self, text, color, align, rect):
        if not text:
            return None
        ui_text = UIText(text, self.font, color, align)
        ui_text.rect.topleft = (rect.x * self.level.tile_width, rect.y * self.level.tile_height)
        return ui_text

    def draw(self, surface):
        level_size_surf = pygame.Surface(self.level.renderer.pixel_size)
        self.screen = level_size_surf
        self.level.draw(level_size_surf)
        self.ui.draw(level_size_surf)

        # self.render(self.title_text, self.title_color, self.__title_rect__, level_size_surf)
        # self.render(self.subtitle_text, self.subtitle_color, self.__subtitle_rect__, level_size_surf)

        pygame.transform.smoothscale(level_size_surf, surface.get_size(), surface)
