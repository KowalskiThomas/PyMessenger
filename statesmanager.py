class StatesManager:
    def __init__(self):
        self.states = dict()

    def SetState(self, id, new_state):
        self.states[id] = new_state

    def GetState(self, id, default = None):
        return self.states.get(id, default)
