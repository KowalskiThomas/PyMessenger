from flask import Flask, Request, Response
from config import use_ssl

class EndpointAction(object):
    def __init__(self):
        # self.action = action
        self.response = Response(status = 200, headers = dict())

    def action(self):
        pass

    def __call__(self, *args):
        self.action()
        return self.response

class HomeHandler(EndpointAction):
    def __init__(self):
        EndpointAction.__init__(self)

    def action(self):
        self.response.data = "coucou"

from threading import Thread
class Server(Thread):
    app = None
    bots = list()

    def __init__(self):
        Thread.__init__(self)
        self.app = Flask("MessengerBotServer")
        self.daemon = True
        self.app.add_url_rule("/", "Home", self.on_home)

        self.bots = list()

    def on_home(self):
        
        for b in self.bots:
            return "ACK"

    def register_bot(self, bot):
        self.bots.append(bot)

    def run(self):
        self.app.run(
            debug = False,
            host = "0.0.0.0",
            port = 5000,
            # ssl_context = (
            #     '/etc/letsencrypt/live/158.ip-51-75-252.eu/fullchain.pem', 
            #     '/etc/letsencrypt/live/158.ip-51-75-252.eu/privkey.pem'
            # )
        )

