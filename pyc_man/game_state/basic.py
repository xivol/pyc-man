from abc import abstractmethod
import pygame
from x_game import XGameState


class BasicState(XGameState):
    @abstractmethod
    def on_did_consume(self, subject, target):
        pass

    def __init__(self, game):
        super().__init__(game)
        self.input.direction = None

    def handle_input_event(self, event):
        super().handle_input_event(event)

        if event.type == pygame.KEYUP:
            self.input.key_up(event)

        if event.type == pygame.KEYDOWN:
            self.input.key_down(event)
