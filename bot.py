import copy

from statesmanager import StatesManager
from server import Server

class Bot:
    handlers = dict()
    states = StatesManager()
    server = Server()

    class User:
        def __init__(self, bot, id):
            self.id = id
            self.bot = bot
 
        def SetState(self, new_state):
            self.bot.states.SetState(self.id, new_state)

        @property
        def State(self):
            return self.bot.states.GetState(self.id)

        def Send(self, data):
            self.bot.send(self.id, data)

    def __init__(self):
        Bot.server.register_bot(self)

    def on_request(self, data):
        data.sender = Bot.User(self, data.sender)
        state = data.sender.State
        if state in self.handlers:
            for f in self.handlers[state]:
                f(self, data)
        else:
            print("Unregistered state: {}".format(state))

    def send(self, user, data):
        print(data)

Bot.server.start()