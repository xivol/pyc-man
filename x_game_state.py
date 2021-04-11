import logging

import pygame
from x_input import XGameInput


def logger_setup(cls, logger=None):
    if not logger:
        cls.logger = logging.getLogger(cls.__name__)
    else:
        cls.logger = logger

class XGameState:
    def __init__(self, logger=None):
        if 'logger' not in self.__class__.__dict__:
            logger_setup(self.__class__, logger)

        self.dirty = True
        self.screen = None
        self.input = XGameInput()

        self.done = False
        self.final = False

        self.next = None
        self.previous = None

        self.persist_keys = set(['input'])

    def setup(self, **persist_values):
        self.logger.info("\tStarting")
        for k, v in persist_values.items():
            self.__setattr__(k, v)
            self.persist_keys.add(k)

    def teardown(self):
        self.done = False
        persist = {}
        for k in self.persist_keys:
            persist[k] = self.__getattribute__(k)
        self.logger.info("\tFinished")
        return persist

    def handle_input_event(self, event):
        if event.type == pygame.KEYUP:
            self.input.key_up(event)

        if event.type == pygame.KEYDOWN:
            self.input.key_down(event)

    def draw(self, surface):
        self.screen = surface
        pass

    def update(self, timedelta):
        pass