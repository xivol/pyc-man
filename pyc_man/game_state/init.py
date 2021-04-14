import pygame

from pyc_man.level import PycManLevel
from pyc_man.objects import Fruits
from pyc_man.actors import PacMan, Ghost
from x_animation_factory import XAnimationFactory
from x_bmpfont import XBMPFont
from x_game_state import XGameState
from x_sprite_factory import XTMXSpriteFactory


class InitState(XGameState):
    def __init__(self, map_file, sprites_file, font_file):
        super().__init__(next="Running",
                         persists={'level',
                                   'sprites',
                                   'animations',
                                   'font',
                                   'bonuses',
                                   'actors'})

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

        self.logger.info(self.actors)

        self.font = XBMPFont(font_file)
        self.done = True
