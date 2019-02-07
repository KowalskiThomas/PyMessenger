class StatesManager:
    def __init__(self):
        self.states = dict()

    def set_state(self, id, new_state):
        self.states[id] = new_state

    def get_state(self, id, default = None):
        return self.states.get(id, default)
