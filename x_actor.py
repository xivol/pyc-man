import x_fsm
import x_object


class XBehavior(x_fsm.XState):
    def __init__(self, animation, **params):
        super().__init__(**params)
        self.animation = animation

    def handle_input(self, actor, timedelta, input, world_state):
        pass

    def enter(self, actor):
        actor.animation.set_state(self.animation)

    def enact(self, actor, timedelta, world_state):
        pass

    def leave(self, actor):
        pass


class XActor(x_object.XAnimatedObject, x_fsm.XFiniteStateManager):
    def __init__(self, animations):
        super().__init__(animations)
        self.sound = None

    @property
    def behavior(self):
        return self.state

    def change_behavior(self, behavior_name):
        if behavior_name not in self.state_dict:
            raise Exception()
        self.state.done = True
        self.state.next = behavior_name

    def setup_behaviors(self, behaviors, init_behavior):
        super().setup_states(behaviors, init_behavior)
        self.state.enter(self)

    def flip_state(self):
        self.state.leave(self)
        super().flip_state()
        self.state.enter(self)

    def update(self, timedelta, *params):
        input = params[0]
        world_state = params[1]
        self.state.handle_input(self, timedelta, input, world_state)
        if self.continues():
            self.state.enact(self, timedelta, world_state)
            self.animate(timedelta)

    def make_sound(self, sounds, sound_name):
        sound = sounds[sound_name]
        if sound.get_num_channels() < 1:
            self.sound = sound.play(fade_ms=100)
