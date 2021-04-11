import datetime
from abc import abstractmethod
import pygame
import logging


class XGame(object):
    __fps__ = 60

    @staticmethod
    def init_screen(width, height):
        return pygame.display.set_mode((width, height), pygame.RESIZABLE)

    @classmethod
    def logger_setup(cls, logger=None):
        if not logger:
            cls.logger = logging.getLogger(cls.__name__)
        else:
            cls.logger = logger

    def __init__(self, title, screen_size, logger=None):
        if 'logger' not in self.__class__.__dict__:
            self.__class__.logger_setup(logger)

        pygame.init()
        pygame.font.init()
        pygame.display.set_caption(title)
        self.screen = XGame.init_screen(*screen_size)
        self.clock = pygame.time.Clock()

        self.running = False
        self.exit_status = 0

        self.state_dict = {}
        self.state_name = None
        self.state = None

    def setup_states(self, state_dict, initial_state):
        self.state_dict = state_dict
        self.state_name = initial_state
        self.state = self.state_dict[self.state_name]

    def handle_input(self):
        try:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.exit_status = 0
                    self.running = False

                self.state.handle_input_event(event)
        except KeyboardInterrupt:
            self.exit_status = 0
            self.running = False

    def flip_state(self):
        previous, self.state_name = self.state_name, self.state.next
        persist_values = self.state.teardown()
        self.state = self.state_dict[self.state_name]
        self.state.setup(**persist_values)
        self.state.previous = previous

    def update(self, deltatime):
        if self.state.final:
            self.running = False
            self.exit_status = 0

        elif self.state.done:
            self.flip_state()
        self.state.update(deltatime)

    def run(self):
        self.running = True
        self.exit_status = 1

        while self.running:
            self.handle_input()

            timedelta = 1000 / self.__fps__
            self.update(timedelta)

            if self.state.dirty:
                self.state.draw(self.screen)
                self.state.dirty = False
                pygame.display.flip()

            self.clock.tick(self.__fps__)

        return self.exit_status
