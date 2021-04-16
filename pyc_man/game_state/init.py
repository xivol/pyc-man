import pygame

from pyc_man.level import PycManLevel
from pyc_man.objects import Fruits
from pyc_man.actors import PacMan, Ghost
from pyc_man.ui import UICounter, UIScoreCounter
from x_animation_factory import XAnimationFactory
from x_bmpfont import XBMPFont
from x_game_state import XGameState
from x_input import Direction
from x_sprite_factory import XTMXSpriteFactory


class InitState(XGameState):
    def __init__(self, map_file, sprites_file, font_file, next_state):
        super().__init__(next=next_state,
                         persists={'level',
                                   'sprites',
                                   'animations',
                                   'actors',
                                   'life_counter',
                                   'level_counter',
                                   'score_counter',
                                   'font',
                                   'bonuses',
                                   'score',
                                   'ui'})

        self.level = PycManLevel(map_file)
        self.sprites = XTMXSpriteFactory(sprites_file)
        self.animations = XAnimationFactory(self.sprites)
        self.font = XBMPFont(font_file)
        self.setup()

    def setup(self, **persist_values):
        super().setup(**persist_values)
        self.level.setup_sprites(self.sprites)

        self.bonuses = list(map(lambda x: self.sprites[x.__sprite_name__].make(x),
                                Fruits.types()))

        for b in self.bonuses:
            self.logger.info("fruit: %s %d", b, b.points())

        self.actors = [
            self.animations.make(PacMan),
            self.animations.make(Ghost)
        ]


        self.life_counter = UICounter(self.sprites['pacman-normal-left'].image, PacMan.__start_lives__)
        self.life_counter.set_position((self.level.tile_width,
                                        (self.level.height - 2) * self.level.tile_height))

        self.level_counter = UICounter([self.sprites[f'fruit-{i}'].image for i in range(1, 9)],
                                       1, 6, Direction.RIGHT)
        self.level_counter.set_position(((self.level.width // 2+1) * self.level.tile_width,
                                         (self.level.height - 2) * self.level.tile_height))

        self.score_counter = UIScoreCounter(self.font, '  score\n{}', 0, align='right')
        self.score = 0

        self.ui = pygame.sprite.Group()
        self.ui.add(self.life_counter, self.level_counter, self.score_counter)

        self.done = True