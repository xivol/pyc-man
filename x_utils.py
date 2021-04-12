import logging


class XLoggingMixin:
    @classmethod
    def logger_setup(cls, logger=None):
        if not logger:
            cls.logger = logging.getLogger(cls.__name__)
        else:
            cls.logger = logger

    def __init__(self, logger):
        if 'logger' not in self.__class__.__dict__:
            self.__class__.logger_setup(logger)