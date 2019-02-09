from classes import Message, QuickReply, ContentType, SetState, ExecuteFunction
from bot import Bot
from decorators import handler


class Paybot(Bot):
    def __init__(self, access_token):
        Bot.__init__(self, access_token)
        self.balances = dict()

    @handler(state = "Home", other_states = [None])
    def handler_home(self, req):
        user = req.sender
        message = req.message

        if not user.id in self.balances:
            self.balances[user.id] = 250

        self.send_home_options(user)

    def send_home_options(self, user):
        user.send(Message(
            content = "What do you want to do?",
            quick_replies=[
                QuickReply("Pay", "Execute:prompt_pay"),
                QuickReply("Get balance", "Execute:send_balance"),
                QuickReply("Something else", "SetState:Advanced")
            ]
        ))

    @handler(state = "Paying")
    def handler_pay(self, req):
        user = req.sender
        message = req.message
        try:
            amount = float(message)
        except ValueError:
            user.send("Désolé, ce montant est invalide. Veuillez réessayer.")
            return

        if amount > self.balances[user.id]:
            user.send("Vous n'avez pas assez d'argent !")
            return

        self.balances[user.id] -= amount
        user.send("Envoi de {}€".format(amount))
        user.set_state("Home")

    def prompt_pay(self, req):
        user = req.sender
        user.send("Combien voulez-vous payer?")
        user.set_state("Paying")

    def send_balance(self, req):
        user = req.sender
        user.send("Votre balance est de {}€".format(self.balances[user.id]))
        user.set_state("Home")

    @handler(state = "Advanced")
    def handler_advanced(self, req):
        req.sender.send(Message(
            content = "Your options are:",
            quick_replies=[
                QuickReply("Delete my account", action = ExecuteFunction(self.delete_action)),
                QuickReply("Send my location", "", ContentType.location),
                QuickReply("Go back", "SetState:Home")
            ]
        ))

    def delete_account(self, req):
        del self.balances[req.sender.id]
        req.sender.send("Okay, we deleted it.")
        req.sender.set_state("Home")
        self.send_home_options(req.sender)

