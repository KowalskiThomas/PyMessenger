import json
import inspect

import requests

from statesmanager import StatesManager
from server import Server
from classes import NotificationType, ContentType, QuickReply, Message
import utils

DEFAULT_API_VERSION = 2.6


class User:
    def __init__(self, bot, id):
        self.id = id
        self.bot = bot

    def SetState(self, new_state):
        self.bot.states.SetState(self.id, new_state)

    @property
    def State(self):
        return self.bot.states.GetState(self.id)

    def Send(self, content):
        self.bot.send(self.id, content)


class Bot:
    handlers = dict()
    states = StatesManager()
    server = Server()

    def __init__(self, access_token, app_secret = None):
        Bot.server.register_bot(self)
        self.api_version = DEFAULT_API_VERSION # kwargs.get('api_version') or DEFAULT_API_VERSION
        self.app_secret = app_secret
        self.graph_url = 'https://graph.facebook.com/v{0}'.format(self.api_version)
        self.access_token = access_token
        self._auth_args = None

    @property
    def auth_args(self):
        if not hasattr(self, '_auth_args'):
            auth = {
                'access_token': self.access_token
            }
            if self.app_secret is not None:
                appsecret_proof = utils.generate_appsecret_proof(self.access_token, self.app_secret)
                auth['appsecret_proof'] = appsecret_proof
            self._auth_args = auth
        return self._auth_args

    def process_quick_reply(self, entry):
        p = entry.quick_reply_payload
        if not p:
            return

        if p.startswith("SetState:"):
            state = p.split(":")[1]
            print("Setting state to {}".format(state))
            entry.sender.SetState(state)
        elif p.startswith("Execute:"):
            f_name = p.split(":")[1]
            to_call = None
            available_functions = inspect.getmembers(self, predicate=inspect.ismethod)
            for name, function in available_functions:
                if name == f_name:
                    to_call = function
                    break

            if to_call:
                print("Executing function {}".format(f_name))
                # Set continue_processing before calling the function so the user can change this behaviour
                entry.continue_processing = False
                to_call(entry)
            else:
                print("Couldn't find function to execute.")
        else:
            print("Unknown payload: {}".format(p))

    def process_payloads(self, entry):
        self.process_quick_reply(entry)

    def on_request(self, data):
        data.sender = User(self, data.sender)
        self.process_payloads(data)
        state = data.sender.State

        if data.continue_processing:
            if state in self.handlers:
                for f in self.handlers[state]:
                    f(self, data)
            else:
                print("Unregistered state: {}".format(state))

    def send(self, user_id, message : Message):
        if isinstance(message, str):
            message = Message(content = message)
        
        assert(isinstance(message, Message))

        payload = dict()
        payload["recipient"] = {
            "id": user_id
        }
        
        if message.content:
            if "message" not in payload: payload["message"] = dict()
            payload["message"]["text"] = message.content

        if message.quick_replies:
            if "message" not in payload: payload["message"] = dict()
            payload["message"]["quick_replies"] = [x.to_dict() for x in message.quick_replies]

        payload["notification_type"] = message.notification_type.value

        print(payload)
        self.send_raw(payload)

    def send_raw(self, payload):
        request_endpoint = '{0}/me/messages'.format(self.graph_url)
        response = requests.post(
            request_endpoint,
            headers = {
                "Authorization": "Bearer {}".format(self.access_token)
            },
            params = self.auth_args,
            json = payload
        )
        result = response.json()
        print(result)
        return result

Bot.server.start()