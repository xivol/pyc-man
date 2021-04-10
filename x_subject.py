from abc import abstractmethod
from x_object import XObject


class XSubject(XObject):
    @abstractmethod
    def act(self, time, input, game_state):
        pass

    def update(self, *args, **kwargs):
        self.act(*args, **kwargs)