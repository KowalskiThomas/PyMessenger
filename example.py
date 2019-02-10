from classes import Message, QuickReply, ContentType, SetState, ExecuteFunction, MessagingEntry
from bot import Bot, User
from decorators import handler


# noinspection PyMethodMayBeStatic
class Paybot(Bot):
    def __init__(self, access_token):
        Bot.__init__(self, access_token)
        self.balances = dict()

    @handler(state = "Home", other_states = [None])
    def handler_home(self, req: MessagingEntry):
        user = req.sender

        if user.id not in self.balances:
            self.balances[user.id] = 250.0

        self.send_home_options(user)

    def send_home_options(self, user: User):
        user.send(Message(
            content = "What do you want to do?",
            quick_replies=[
                QuickReply("Pay", ExecuteFunction(self.prompt_pay)),
                QuickReply("Get balance", ExecuteFunction(self.send_balance)),
                QuickReply("Something else", SetState("Advanced"))
            ]
        ))

    @handler(state = "Paying")
    def handler_pay(self, req: MessagingEntry):
        user = req.sender
        message = req.message
        try:
            amount = float(message)
        except ValueError:
            user.send("Sorry, but this amount is invalid. Please try again.")
            return

        if amount > self.balances[user.id]:
            user.send("Your balance is insufficient.")
            return

        self.balances[user.id] -= amount
        user.send("Sending {}€".format(amount))
        user.set_state("Home")
        print("State after handler_pay: {}".format(user.state))
        req.continue_processing = True

    def prompt_pay(self, req: MessagingEntry):
        user = req.sender
        user.send("How much do you want to send?")
        user.set_state("Paying")

    def send_balance(self, req: MessagingEntry):
        user = req.sender
        user.send("Your balance is {}€".format(self.balances[user.id]))
        user.set_state("Home")
        req.continue_processing = True

    @handler(state = "Advanced")
    def handler_advanced(self, req: MessagingEntry):
        req.sender.send(Message(
            content = "Your options are:",
            quick_replies=[
                QuickReply("Delete my account", action = ExecuteFunction(self.delete_account)),
                QuickReply("Send my location", payload = "", content_type = ContentType.location),
                QuickReply("Go back", SetState("Home"))
            ]
        ))

    def delete_account(self, req: MessagingEntry):
        del self.balances[req.sender.id]
        req.sender.send("Okay, we deleted it.")
        req.sender.set_state("Home")
        req.continue_processing = True
