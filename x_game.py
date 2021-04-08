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

        self.renderer = None
        self.running = False
        self.dirty = False
        self.exit_status = 0

    @abstractmethod
    def draw(self, surface):
        pass

    def update(self, timedelta):
        pass

    def handle_input_event(self, event):
        pass

    def handle_input(self):
        try:
            event = pygame.event.wait()
            self.handle_input_event(event)
        except KeyboardInterrupt:
            self.exit_status = 0
            self.running = False

    def run(self):
        """ This is our app main loop
        """
        self.dirty = True
        self.running = True
        self.exit_status = 1

        while self.running:
            self.handle_input()

            timedelta = 1000 / self.__fps__
            self.update(timedelta)

            # we don't want to constantly draw on the display, as that is way
            # inefficient.  so, this 'dirty' values is used.  If dirty is True,
            # then re-render the map, display it, then mark 'dirty' False.
            if self.dirty:
                self.draw(self.screen)
                self.dirty = False
                pygame.display.flip()

            self.clock.tick(self.__fps__)

        return self.exit_status
