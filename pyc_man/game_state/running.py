import pygame

from pyc_man.objects import Bonus, Pellet, Energizer
from pyc_man.subjects import PacMan, ConsumeHandler
from x_game_state import XGameState
from x_input import Direction


class RunningState(XGameState, ConsumeHandler):
    def __init__(self):
        super().__init__()

        # Persistent values
        self.level = None
        self.sprites = None
        self.actors = None
        self.font = None
        self.bonuses = None
        self.score = 0
        self.fruit = None
        self.pellets_count = 0
        self.current_bonus = 0

    def setup(self, **persist_values):
        super().setup(**persist_values)
        self.level.setup_sprites(self.sprites)
        for actor in self.actors:
            self.level.spawn(actor)

        self.input.direction = None

    def teardown(self):
        self.persist_keys |= {'score', 'pellets_count', 'current_bonus'}
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
        for actor in self.actors:
            actor.update(timedelta, self.input, self)
        if self.fruit:
            self.fruit.update(timedelta)
        self.dirty = True

    def draw(self, surface):
        temp = pygame.Surface(self.level.renderer.pixel_size)
        self.screen = temp
        self.level.draw(temp)

        text = self.font.render(f'  score\n{self.score}', align='right')
        temp.blit(text, (0, 0))

        pygame.transform.smoothscale(temp, surface.get_size(), surface)

    def on_did_consume(self, subject, target):
        if isinstance(subject, PacMan) and isinstance(target, Bonus):
            self.add_score(target.points)
            self.level.remove(target)
            if isinstance(target, Pellet) or isinstance(target, Energizer):
                self.add_pellet_count(1)
                if self.level.pellets == 0:
                    self.done = True
                    self.next = "Win"

    def add_score(self, points):
        self.score += points

    def add_pellet_count(self, count):
        self.pellets_count += count
        if self.pellets_count == 70:
            self.fruit = self.level.spawn(self.bonuses[self.current_bonus])
            self.current_bonus += 1
            if self.current_bonus == len(self.bonuses):
                self.current_bonus = len(self.bonuses) - 1
