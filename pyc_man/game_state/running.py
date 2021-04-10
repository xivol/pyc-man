import pygame

from pyc_man.objects import Bonus
from pyc_man.subjects import PacMan
from x_game_state import XGameState
from x_input import Direction


class RunningState(XGameState):
    def __init__(self):
        super().__init__()
        self.score = 0
        self.pellets_count = 0
        self.level = None
        self.sprites = None
        self.actors = None
        self.font = None
        self.bonuses = None

    def setup(self, **persist_values):
        super().setup(**persist_values)
        self.setup_actors()

    def setup_actors(self):
        for actor in self.actors:
            self.level.spawn(actor)

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
            subject.points += target.points
            self.set_score(subject.points)
            self.level.remove(target)

    def set_score(self, points):
        print(points)
        self.score = points