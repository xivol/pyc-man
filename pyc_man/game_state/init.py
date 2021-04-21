import pygame

from pyc_man.behaviors import NormalPacMan, DyingPacMan, MovingPacMan, ChaseGhost, FrightGhost
from pyc_man.level import PycManLevel
from pyc_man.objects import Fruits
from pyc_man.actors import PacMan, Ghost
from pyc_man.ui import UICounter, UIScoreCounter
from x_animation_factory import XAnimationFactory
from x_bmpfont import XBMPFont
from x_game_state import XGameState
from x_input import Direction
from x_sound import XSoundManager
from x_sprite_factory import XTMXSpriteFactory


class InitState(XGameState):
    def __init__(self, map_file, sprites_file, font_file, sounds_dir, next_state):
        super().__init__(next=next_state,
                         persists={'sprites',
                                   'animations',
                                   'sounds',
                                   'level',
                                   'actors',
                                   'font',
                                   'ui', 'life_counter', 'level_counter', 'score_counter',
                                   'bonuses',
                                   'score'})

        self.level = PycManLevel(map_file)
        self.sprites = XTMXSpriteFactory(sprites_file)
        self.animations = XAnimationFactory(self.sprites)
        self.sounds = XSoundManager(sounds_dir)
        self.font = XBMPFont(font_file)
        self.setup()

    def setup(self, **persist_values):
        super().setup(**persist_values)
        self.level.setup_sprites(self.sprites)

        self.bonuses = list(map(lambda x: self.sprites[x.__sprite_name__].make(x),
                                Fruits.types()))

        for b in self.bonuses:
            self.logger.info("fruit: %s %d", b, b.points())

        pacman = self.animations.make(PacMan)
        pacman.setup_behaviors({
            'init': NormalPacMan('init'),
            'normal': NormalPacMan('normal'),
            'dying': DyingPacMan('dead', sound='death'),
            'moving': MovingPacMan(PacMan.__speed__, 'moving')
        }, 'init')
        ghost = self.animations.make(Ghost)
        ghost.setup_behaviors({
            "chase": ChaseGhost(Ghost.__speed__, "normal"),
            "fright": FrightGhost("frighten-normal", 1000)
        }, "chase")

        self.actors = [
            pacman,
            ghost
        ]

        self.life_counter = UICounter(self.sprites['pacman-normal-left'].image, PacMan.__start_lives__)
        self.life_counter.set_position((self.level.tile_width,
                                        (self.level.height - 2) * self.level.tile_height))

        self.level_counter = UICounter([self.sprites[f'fruit-{i}'].image for i in range(1, 9)],
                                       1, 0, 6, Direction.RIGHT)
        self.level_counter.set_position(((self.level.width // 2+1) * self.level.tile_width,
                                         (self.level.height - 2) * self.level.tile_height))

        self.score_counter = UIScoreCounter('  score\n{}', 0, self.font, None, 'right')

        self.ui = pygame.sprite.Group()
        self.ui.add(self.life_counter, self.level_counter, self.score_counter)

        self.score = 0
        self.current_bonus = 0
        self.pellets_count = 0

        self.done = True