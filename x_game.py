import pygame
import logging
import x_fsm


class XGame(x_fsm.XFiniteStateManager):
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

        super().__init__()

        pygame.init()
        pygame.font.init()
        pygame.display.set_caption(title)
        self.screen = XGame.init_screen(*screen_size)
        self.clock = pygame.time.Clock()

        self.running = False
        self.exit_status = 0

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

    def update(self, deltatime):
        if not self.continues():
            self.running = False
            self.exit_status = 0
        else:
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
