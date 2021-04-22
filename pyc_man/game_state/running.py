import pygame

from pyc_man.behaviors import ConsumeHandler, ChaseGhost
from pyc_man.objects import BonusMixin, Pellet, Energizer, Fruits
from pyc_man.actors import PacMan, Ghost
from x_game_state import XGameState
from x_input import Direction


class RunningState(XGameState, ConsumeHandler):
    def __init__(self, persists=set()):
        super().__init__(persists=persists | {'score', 'pellets_count', 'current_bonus'})

        # Persistent values
        self.level = None
        self.sprites = None
        self.actors = None
        self.font = None
        self.bonuses = None
        self.sounds = None
        self.ui = None
        self.life_counter = None
        self.level_counter = None
        self.score_counter = None

        self.score = 0
        self.pellets_count = 0
        self.current_bonus = 0
        self.fruit = None

    def setup(self, **persist_values):
        super().setup(**persist_values)
        self.life_counter.set_value(self.actors[0].extra_lives)
        self.level_counter.set_value(self.current_bonus + 1)

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
            if isinstance(target, Energizer):
                self.done = True
                self.next = "Fright"

    def add_score(self, points):
        self.score += points
        self.score_counter.set_value(self.score)

    def add_pellet_count(self, count):
        self.pellets_count += count
        if self.pellets_count == 70 or self.pellets_count == 170:
            if not self.fruit:
                self.fruit = self.level.spawn(self.bonuses[self.current_bonus])
            elif not self.fruit.alive():
                self.fruit = self.level.spawn(self.bonuses[self.current_bonus])
