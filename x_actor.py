import x_fsm
import x_object
import x_sound


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


class XActor(x_object.XAnimatedObject, x_fsm.XFiniteStateManager,
             x_sound.XSoundMixin):
    __behaviors__ = None
    __default_behavior__ = None
    __sounds__ = None

    def __init__(self, animations):
        super().__init__(animations)
        x_fsm.XFiniteStateManager.__init__(self)
        x_sound.XSoundMixin.__init__(self)

    @property
    def behavior(self):
        return self.state

    def change_behavior(self, behavior_name):
        if behavior_name not in self.state_dict:
            raise Exception()
        if self.state_name != behavior_name:
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

    def play_sound(self, event, channel):
        if channel.sound() is not self.sounds[event]:
            channel.play(self.sounds[event])


class XActorFactory:
    def __init__(self, sprites, animations, sounds):
        self.sprites = sprites
        self.animations = animations
        self.sounds = sounds

    def make(self, type):
        if not issubclass(type, XActor):
            raise Exception
        man = type.__manager_type__(type.__sprite_name__,
                                    self.animations,
                                    type.__animations__,
                                    type.__default_anim__)
        actor = type(man)
        actor.setup_behaviors(type.__behaviors__, type.__default_behavior__)
        if type.__sounds__:
            actor.setup_sounds(self.sounds, type.__sounds__)
        return actor