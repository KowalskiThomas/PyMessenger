from classes import Message, QuickReply
from bot import Bot
from decorators import handler


class Paybot(Bot):
    def __init__(self, access_token):
        Bot.__init__(self, access_token)

    @handler(state = "Home", other_states = [None])
    def handler_home(self, req):
        user = req.sender
        message = req.message
        print(message)
        user.Send(Message(
            content = "What do you want to do?",
            quick_replies=[
                QuickReply("Pay", "Execute:prompt_pay"),
                QuickReply("Something else", "SetState:Home")
            ]
        ))
        user.SetState("Pay")

    @handler(state = "Pay")
    def handler_pay(self, req):
        user = req.sender
        message = req.message
        try:
            amount = float(message)
        except:
            user.Send("Désolé, ce montant est invalide. Veuillez réessayer.")

        user.Send("Envoi de {}".format(amount))
        user.SetState("Home")


    # @handler(state = "PromptPay")
    def prompt_pay(self, req):
        user = req.sender
        user.Send("Combien voulez-vous payer?")
        user.SetState("Pay")
