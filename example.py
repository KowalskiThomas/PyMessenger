from bot import Bot
from decorators import handler

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

