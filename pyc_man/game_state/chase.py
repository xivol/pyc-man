from pyc_man.actors import Ghost, PacMan
from pyc_man.game_state import RunningState


class ChaseState(RunningState):
    def setup(self, **persist_values):
        super().setup(**persist_values)
        for actor in filter(lambda x: isinstance(x, Ghost), self.actors):
            if actor.is_alive:
                actor.change_behavior(Ghost.Behavior.CHASE)

    def on_did_consume(self, subject, target):
        if isinstance(subject, Ghost) and isinstance(target, PacMan):
            target.change_behavior(target.Behavior.DEAD)
            self.done = True
            if target.extra_lives > 0:
                self.next = "Lose"
            else:
                self.next = "GameOver"
