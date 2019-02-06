import copy

class StatesManager:
    def __init__(self):
        self.states = dict()

    def SetState(self, id, new_state):
        self.states[id] = new_state

    def GetState(self, id, default = None):
        return self.states.get(id, default)

class Bot:
    handlers = dict()
    states = StatesManager()

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
        pass

    def on_req(self, user, req):
        user = Bot.User(self, user)
        state = user.State
        if state in self.handlers:
            for f in self.handlers[state]:
                f(self, user, req)
        else:
            print("Unregistered state: {}".format(state))

    def send(self, user, data):
        print(data)

def handler(*args, **kwargs):
    if "other_states" in kwargs:
        states = kwargs["other_states"]
    else:
        states = list()

    if not "state" in kwargs:
        raise Exception("A handler must provide a state parameter.")
    states.append(kwargs["state"])

    
    def decorator(func):
        for state in states:
            if not state in Bot.handlers:
                Bot.handlers[state] = list()
            
            Bot.handlers[state].append(func)
        print("Registering handler: {} for {}".format(func.__name__, kwargs))

    return decorator

class Paybot(Bot):
    def __init__(self):
        Bot.__init__(self)

    @handler(state = "Home", other_states = [None])
    def handler_home(self, user, req):
        if req == "pay":
            user.Send("How much?")
            user.SetState("Pay")

    @handler(state = "Pay")
    def handler_pay(self, user, req):
        if req == "cancel":
            user.Send("OK. Cancelling.")
            user.SetState("Home")
        else:
            amount = float(req)
            user.Send("Paying {}".format(amount))
            user.SetState("Home")

USER = 1
try:
    b = Paybot()
    while True:
        req = input("Bot1>")
        b.on_req(USER, req)
except KeyboardInterrupt:
    print()
except EOFError:
    print()