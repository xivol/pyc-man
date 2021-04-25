from pyc_man.actors import Ghost, PacMan
from .running import RunningState


class ChaseState(RunningState):
    __music_loop__ = 'ghost_chase_1'

    def setup(self, **persist_values):
        super().setup(**persist_values)
        for actor in filter(lambda x: isinstance(x, Ghost), self.actors):
            if actor.is_alive:
                actor.change_behavior(Ghost.Behavior.CHASE)
