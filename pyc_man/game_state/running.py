import pygame

from pyc_man.objects import BonusMixin, Pellet, Energizer
from pyc_man.actors import PacMan, ConsumeHandler, Ghost
from x_game_state import XGameState
from x_input import Direction


class RunningState(XGameState, ConsumeHandler):
    def __init__(self):
        super().__init__(persists={'score', 'pellets_count', 'current_bonus'})

        # Persistent values
        self.level = None
        self.sprites = None
        self.actors = None
        self.font = None
        self.bonuses = None
        self.life_counter = None
        self.level_counter = None
        self.score_counter = None

        self.score = 0
        self.pellets_count = 0
        self.current_bonus = 0
        self.fruit = None

    def setup(self, **persist_values):
        super().setup(**persist_values)

        for actor in self.actors:
            if not actor.is_alive:
                actor.revive()
            self.level.spawn(actor)
        self.life_counter.set_value(self.actors[0].lives)
        self.level_counter.set_value(self.current_bonus + 1)
        self.input.direction = None

    def teardown(self):
        if self.fruit:
            self.level.remove(self.fruit)
            self.fruit = None
        return super().teardown()

    def handle_input_event(self, event):
        super().handle_input_event(event)

        if event.type == pygame.KEYUP:
            self.input.direction = None

        if self.input.keys_pressed:
            if pygame.K_UP in self.input.keys_pressed:
                self.input.direction = Direction.UP
            elif pygame.K_DOWN in self.input.keys_pressed:
                self.input.direction = Direction.DOWN
            elif pygame.K_RIGHT in self.input.keys_pressed:
                self.input.direction = Direction.RIGHT
            elif pygame.K_LEFT in self.input.keys_pressed:
                self.input.direction = Direction.LEFT

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.input.direction = Direction.UP
            elif event.key == pygame.K_DOWN:
                self.input.direction = Direction.DOWN
            elif event.key == pygame.K_RIGHT:
                self.input.direction = Direction.RIGHT
            elif event.key == pygame.K_LEFT:
                self.input.direction = Direction.LEFT

    def update(self, timedelta):
        self.level.update(timedelta, self.input, self)
        self.dirty = True

    def draw(self, surface):
        temp = pygame.Surface(self.level.renderer.pixel_size)
        self.screen = temp
        self.level.draw(temp)
        self.ui.draw(temp)
        # text = self.font.render(f'  score\n{self.score}', align='right')
        # temp.blit(text, (0, 0))

        # for i in range(self.actors[0].lives-1):
        #     temp.blit(self.life_counter, ((i + 1) * 32, (self.level.height - 2) * self.level.tile_height))

        pygame.transform.smoothscale(temp, surface.get_size(), surface)

    def on_did_consume(self, subject, target):
        if isinstance(subject, PacMan) and isinstance(target, BonusMixin):
            self.add_score(target.points())
            self.level.remove(target)
            if isinstance(target, Pellet) or isinstance(target, Energizer):
                self.add_pellet_count(1)
                if self.level.pellets == 0:
                    self.done = True
                    self.next = "Win"
                    self.current_bonus += 1
                    if self.current_bonus == len(self.bonuses):
                        self.current_bonus = len(self.bonuses) - 1

        elif isinstance(subject, Ghost) and isinstance(target, PacMan):
            target.die()
            self.done = True
            if target.lives > 1:
                self.next = "Lose"
            else:
                self.next = "GameOver"

    def add_score(self, points):
        self.score += points
        self.score_counter.set_value(self.score)

    def add_pellet_count(self, count):
        self.pellets_count += count
        if (self.pellets_count == 70 or self.pellets_count == 170) and \
                not self.fruit:
            self.fruit = self.level.spawn(self.bonuses[self.current_bonus])
