import time

from classes import Message, QuickReply, ContentType, SetState, ExecuteFunction, MessagingEntry
from bot import Bot, User
from decorators import handler


# noinspection PyMethodMayBeStatic
class Paybot(Bot):
    def __init__(self, access_token):
        Bot.__init__(self, access_token)
        self.balances = dict()
        self.emails = dict()
        self.receivers = dict()

    @handler(state = "Home", other_states = [None])
    def handler_home(self, req: MessagingEntry):
        user = req.sender

        if user.id not in self.balances:
            self.send_signup(user)
        else:
            self.send_home_options(user)

    def send_signup(self, user):
        user.send(Message(
            content = "Welcome to PayBot! What's your email?",
            quick_replies=[
                QuickReply("", action=ExecuteFunction(self.save_email), content_type=ContentType.email)
            ]
        ))
        user.set_state("WaitingEmail")
        

    def send_home_options(self, user: User):
        user.send(Message(
            content = "What do you want to do?",
            quick_replies=[
                QuickReply("Pay", ExecuteFunction(self.prompt_pay)),
                QuickReply("Get balance", ExecuteFunction(self.send_balance)),
                QuickReply("Something else", SetState("Advanced"))
            ]
        ))

    @handler(state = "WaitingEmail")
    def handler_custom_email(self, req:MessagingEntry):
        req.sender.send(Message(
            content = "Thanks for signing up! You just got $250!"
        ))

        self.balances[req.sender.id] = 250.0
        self.emails[req.sender.id] = req.message
        req.sender.set_state("Home")
        req.continue_processing = True

    def save_email(self, req:MessagingEntry):
        email = req.quick_reply_payload
        req.message = email
        self.handler_custom_email(req)

    def prompt_pay(self, req: MessagingEntry):
        user = req.sender
        user.send("Who do you want to pay?")
        user.set_state("WaitingReceiver")

    @handler(state = "WaitingReceiver")
    def handler_set_receiver(self, req:MessagingEntry):
        user = req.sender
        message = req.message

        if not message in self.emails.values():
            user.send("I don't know this person!")
            return

        receiver_id = [k for k, v in self.emails.items() if v == message][0]
        self.receivers[user.id] = receiver_id

        user.send("How much do you want to send?")
        user.set_state("Paying")

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

        receiver_id = self.receivers[user.id]
        print("Sending {} from {} to {}".format(
            amount,
            self.emails[user.id],
            self.emails[receiver_id]
        ))
        self.balances[receiver_id] += amount
        self.balances[user.id] -= amount
        user.send("Sending ${}".format(amount))
        user.set_state("Home")
        req.continue_processing = True

    def send_balance(self, req: MessagingEntry):
        user = req.sender
        user.send("Your balance is ${}".format(self.balances[user.id]))
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
