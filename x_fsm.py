

class XState(object):
    def __init__(self, next=None, previous=None, persists=set()):
        self.done = False
        self.final = False

        self.next = next
        self.previous = previous

        self.persist_keys = set(persists)

    def setup(self, **persist_values):
        for k, v in persist_values.items():
            self.__setattr__(k, v)
            self.persist_keys.add(k)

    def teardown(self):
        persist_values = {}
        for k in self.persist_keys:
            persist_values[k] = self.__getattribute__(k)
        self.done = False
        return persist_values


class XFiniteStateManager(object):
    def __init__(self):
        self.state_dict = {}
        self.state_name = None
        self.state = None

    def setup_states(self, state_dict, initial_state):
        self.state_dict = state_dict
        self.state_name = initial_state
        self.state = self.state_dict[self.state_name]

    def flip_state(self):
        previous, self.state_name = self.state_name, self.state.next
        persist_values = self.state.teardown()

        self.state = self.state_dict[self.state_name]
        self.state.setup(**persist_values)
        self.state.previous = previous

    def continues(self):
        if self.state.final:
            return False
        elif self.state.done:
            self.flip_state()
        return True
