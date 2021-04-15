import pygame

from pyc_man.level import PycManLevel
from pyc_man.objects import Fruits
from pyc_man.actors import PacMan, Ghost
from x_animation_factory import XAnimationFactory
from x_bmpfont import XBMPFont
from x_game_state import XGameState
from x_sprite_factory import XTMXSpriteFactory


class InitState(XGameState):
    def __init__(self, map_file, sprites_file, font_file, next_state):
        super().__init__(next=next_state,
                         persists={'level',
                                   'sprites',
                                   'animations',
                                   'actors',
                                   'life_counter',
                                   'font',
                                   'bonuses',
                                   'score'})

        self.level = PycManLevel(map_file)

        self.sprites = XTMXSpriteFactory(sprites_file)

        self.level.setup_sprites(self.sprites)

        self.animations = XAnimationFactory(self.sprites)

        self.bonuses = list(map(lambda x: self.sprites[x.__sprite_name__].make(x),
                                Fruits.types()))
        for b in self.bonuses:
            self.logger.info("fruit: %s %d", b, b.points())

        self.actors = [
            self.animations.make(PacMan),
            self.animations.make(Ghost)
        ]

        self.life_counter = self.sprites['pacman-normal-left'].image

        self.font = XBMPFont(font_file)

        self.score = 0

        self.done = True

    def setup(self, **persist_values):
        super().setup(**persist_values)
        self.done = True