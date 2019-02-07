from classes import Message, QuickReply, ContentType
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
        user.send(Message(
            content = "What do you want to do?",
            quick_replies=[
                QuickReply("Pay", "Execute:prompt_pay"),
                QuickReply("Something else", "SetState:Home"),
                QuickReply("Email", "SetState:GotEmail", ContentType.email),
                QuickReply("Location", "SetState:GotLocation", ContentType.location),
                QuickReply("Phone Number", "SetState:GotPhoneNumber", ContentType.phone_number)
            ]
        ))

    @handler(state = "Pay")
    def handler_pay(self, req):
        user = req.sender
        message = req.message
        try:
            amount = float(message)
        except:
            user.send("Désolé, ce montant est invalide. Veuillez réessayer.")
            return

        user.send("Envoi de {}".format(amount))
        user.set_state("Home")


    # @handler(state = "PromptPay")
    def prompt_pay(self, req):
        user = req.sender
        user.send("Combien voulez-vous payer?")
        user.set_state("Pay")
