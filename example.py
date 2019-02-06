from bot import Bot
from decorators import handler

class Paybot(Bot):
    def __init__(self):
        Bot.__init__(self)

    @handler(state = "Home", other_states = [None])
    def handler_home(self, req):
        user = req.sender
        message = req.message
        print(message)
        if message == "pay":
            user.Send("How much?")
            user.SetState("Pay")

    @handler(state = "Pay")
    def handler_pay(self, req):
        user = req.sender
        message = req.message
        if message == "cancel":
            user.Send("OK. Cancelling.")
            user.SetState("Home")
        else:
            amount = float(message)
            user.Send("Paying {}".format(amount))
            user.SetState("Home")

