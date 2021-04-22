from pyc_man.actors import Ghost, PacMan
from pyc_man.behaviors import FrightGhost
from pyc_man.game_state import RunningState
from pyc_man.objects import Energizer
from x_input import Direction


class FrightState(RunningState):
    def __init__(self, duration, timeout_after=None):
        super().__init__(persists={'fright_duration', 'fright_timeout'})
        self.fright_duration = duration * 1000  # ms
        if timeout_after and timeout_after < duration:
            self.fright_timeout = timeout_after / duration
        else:
            self.fright_timeout = 0.75
        self.time_since_start = 0
        self.streak = 0
        self.ghosts = None

    def setup(self, **persist_values):
        super().setup(**persist_values)
        self.time_since_start = 0
        self.streak = 0
        self.ghosts = filter(lambda x: isinstance(x, Ghost), self.actors)
        for actor in self.ghosts:
            if actor.is_alive:
                actor.change_behavior(Ghost.Behavior.FRIGHT)

    def update(self, timedelta):
        super().update(timedelta)
        self.time_since_start += timedelta
        if self.time_since_start >= self.fright_duration:
            self.done = True
            self.next = Ghost.Behavior.CHASE
        elif self.time_since_start >= \
                self.fright_timeout * self.fright_duration:
            flicker_ghosts = filter(lambda x: isinstance(x.behavior, FrightGhost),
                                    self.ghosts)
            for actor in flicker_ghosts:
                actor.behavior.start_timeout()

    def on_did_consume(self, actor, target):
        if isinstance(actor, PacMan) and isinstance(target, Ghost):
            self.streak += 1
            self.add_score(target.points() * self.streak)
            target.change_behavior(target.Behavior.DEAD)
            if self.streak == sum(1 for a in self.ghosts):
                self.streak = 0
        else:
            super().on_did_consume(actor, target)