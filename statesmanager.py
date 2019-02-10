class StatesManager:
    def __init__(self):
        self.states = dict()

    def set_state(self, id_, new_state):
        self.states[id_] = new_state

    def get_state(self, id_, default = None):
        return self.states.get(id_, default)
