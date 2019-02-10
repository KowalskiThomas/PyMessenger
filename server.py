import sys
from threading import Thread
import json
from flask import Flask, Request, Response, request

from log import Log
from parser import parse_raw_data

VERIFY_TOKEN = "mliqlmskdlqmskdlmqsclmkqsnfhqzopkdqlmskqsfjhqsufqlksjklqzlkdjqlksjdlqksjdliqzjpodqs"


class Server(Thread):
    app = None
    bots = list()

    def __init__(self):
        Thread.__init__(self, name = "MessengerBotServer")
        self.app = Flask("MessengerBotServer")
        self.daemon = True
        self.app.register_error_handler(500, self.handle_500)
        self.app.add_url_rule("/", "Home", self.on_home, methods = ["GET", "POST"])

        self.bots = list()
        
    def handle_500(self, error):
        return json.dumps({
            "status": 500,
            "message": str(error)
        })

    def on_home(self):
        if request.method == 'GET':
            Log.info("Token verification request")
            token_sent = request.args.get("hub.verify_token")
            return self.verify_fb_token(token_sent)
        else:
            data = request.get_json()
            try:
                for chunk in parse_raw_data(data):
                    for b in self.bots:
                        b.on_request(chunk)
            except KeyError as e:
                print("Exception while processing request.", e)
                return json.dumps({
                    "status": 500,
                    "response": "Exception raised while processing request."
                })

            return json.dumps({
                "status": 200,
                "response": "Message processed."
            })

    @staticmethod
    def verify_fb_token(token_sent):
        if token_sent == VERIFY_TOKEN:
            return request.args.get("hub.challenge")
        
        return json.dumps({
            "status": 403,
            "message": "Invalid verify token."
        })

    def register_bot(self, bot):
        self.bots.append(bot)

    def run(self):
        try:
            self.app.run(
                debug = False,
                host = "0.0.0.0",
                port = 5000,
                ssl_context = (
                    '/etc/letsencrypt/live/158.ip-51-75-252.eu/fullchain.pem', 
                    '/etc/letsencrypt/live/158.ip-51-75-252.eu/privkey.pem'
                )
            )
        except PermissionError as e:
            print("!!!!!!!!!!!!!!!! Couldn't start internal web server.")
            sys.exit(1)