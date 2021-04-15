import logging

import pygame
from x_input import XGameInput
from x_utils import XLoggingMixin
from x_fsm import XState


class XGameState(XState, XLoggingMixin):
    def __init__(self, next=None, previous=None, persists=set(), logger=None):
        self.__class__.logger_setup(logger)
        super().__init__(next, previous, persists | {'input'})

        self.dirty = True
        self.screen = None
        self.input = XGameInput()

    def setup(self, **persist_values):
        self.logger.info("\tStarting")
        self.dirty = True
        super().setup(**persist_values)

    def teardown(self):
        self.logger.info("\tFinished")
        return super().teardown()

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