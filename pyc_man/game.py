import math
import pygame

from pyc_man.game_state import RunningState
from x_bmpfont import XBMPFont
from x_game import XGame
from x_sprite_factory import XSpriteFactory

from pyc_man.objects import Fruits, Bonus
from pyc_man.subjects import PacMan
from pyc_man.level import PycManLevel


def wrap(x, y, width, height):
    if not 0 <= x < width:
        x = (x + width) % width
    if not 0 <= y < height:
        y = (y + height) % height
    return x, y


class PycManGame(XGame):
    @staticmethod
    def __dimensions__(w,h):
        f = math.gcd(w, h)
        if w // f != 7 or h // f != 9:
            if h >= w:
                w = 7 * h // 9
            else:
                h = 9 * w // 7
        return w, h

    def __init__(self, screen_size, map_file, sprites_file, font_file):
        super().__init__('Pyc-Man',
                         PycManGame.__dimensions__(*screen_size),
                         RunningState)
        self.level = PycManLevel(map_file)
        self.sprites = XSpriteFactory(sprites_file)
        self.level.setup_sprites(self.sprites)

        self.font = XBMPFont(font_file)

        self.actors = pygame.sprite.Group()
        self.setup_actors()

        self.bonuses = [self.sprites[Fruits.sprite_name(i)].make(Fruits, order=i)
                        for i in range(Fruits.count())]

        self.score = 0

    def setup_actors(self):
        actors = [
            self.sprites['pacman-left'][0].make(PacMan)
        ]

        for actor in actors:
            self.level.spawn(actor)
            self.actors.add(actor)

    def draw(self, surface):
        temp = pygame.Surface(self.level.renderer.pixel_size)
        self.state.screen = temp
        self.level.draw(temp)
        text = self.font.render(f'  score\n{self.score}', align='right')
        temp.blit(text,(0, 0))
        pygame.transform.smoothscale(temp, surface.get_size(), surface)

    def update(self, timedelta):
        self.actors.update(timedelta, self.state.input, self.state)
        self.dirty = True

    def set_score(self, points):
        print(points)
        self.score = points


