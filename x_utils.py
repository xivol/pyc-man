import logging


class XLoggingMixin:
    @classmethod
    def logger_setup(cls, logger=None):
        if 'logger' not in cls.__dict__:
            if not logger:
                cls.logger = logging.getLogger(cls.__name__)
            else:
                cls.logger = logger
        elif logger:
            cls.logger = logger