import pygame
from x_input import XGameInput


class XGameState:
    def __init__(self):
        self.dirty = True
        self.screen = None
        self.input = XGameInput()

        self.done = False
        self.quit = False
        self.next = None
        self.previous = None
        self.persist_keys = set()

    def setup(self, **persist_values):
        for k, v in persist_values:
            self.__setattr__(k, v)
            self.persist_keys.add(k)

    def teardown(self):
        self.done = False
        persist = {}
        for k in self.persist_keys:
            persist[k] = self.__getattribute__(k)
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