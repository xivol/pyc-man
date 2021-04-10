import pygame

from pyc_man.level import PycManLevel
from pyc_man.objects import Fruits
from pyc_man.subjects import PacMan
from x_bmpfont import XBMPFont
from x_game_state import XGameState
from x_sprite_factory import XSpriteFactory


class InitState(XGameState):
    def __init__(self, map_file, sprites_file, font_file):
        super().__init__()

        self.level = PycManLevel(map_file)
        self.sprites = XSpriteFactory(sprites_file)
        self.level.setup_sprites(self.sprites)
        self.font = XBMPFont(font_file)

        self.bonuses = [self.sprites[Fruits.sprite_name(i)].make(Fruits, order=i)
                        for i in range(Fruits.count())]
        self.actors = [
            self.sprites['pacman-left'][0].make(PacMan)
        ]

        self.next = "Running"
        self.done = True

    def teardown(self):
        self.persist_keys |= ['level', 'sprites', 'font', 'bonuses', 'actors']
        super().teardown()
