import inspect

import requests

from statesmanager import StatesManager
from server import Server
from classes import NotificationType, ContentType, QuickReply, Message, MessagingEntry
import utils

DEFAULT_API_VERSION = 2.6


class User:
    def __init__(self, bot, id):
        self.id = id
        self.bot = bot

    def set_state(self, new_state):
        self.bot.states.set_state(self.id, new_state)

    @property
    def state(self):
        return self.bot.states.get_state(self.id)

    def send(self, content):
        self.bot.send(self.id, content)


class Bot:
    handlers = dict()
    states = StatesManager()
    server = Server()

    def __init__(self, access_token, app_secret = None, api_version = None):
        Bot.server.register_bot(self)
        self.api_version = api_version if api_version else DEFAULT_API_VERSION
        self.app_secret = app_secret
        self.graph_url = 'https://graph.facebook.com/v{0}'.format(self.api_version)
        self.access_token = access_token
        self._auth_args = None

        self.always_typing_on = False
        self.always_mark_seen = False

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
            entry.sender.set_state(state)
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

    def process_payloads(self, entry: MessagingEntry):
        self.process_quick_reply(entry)

    def on_request(self, data: MessagingEntry):
        data.sender = User(self, data.sender)

        if self.always_typing_on:
            self.typing_on(data.sender)

        if self.always_mark_seen:
            self.mark_seen(data.sender)

        self.process_payloads(data)
        state = data.sender.state

        if data.continue_processing:
            if state in self.handlers:
                for f in self.handlers[state]:
                    f(self, data)
            else:
                print("Unregistered state: {}".format(state))

    def send(self, user_id, message: Message):
        if isinstance(message, str):
            message = Message(content = message)
        
        assert(isinstance(message, Message))

        payload = {
            "recipient": {
               "id": user_id
            },
            "message": dict(),
            "notification_type": message.notification_type.value,
            "messaging_type": message.message_type.value
        }
        
        if message.content:
            payload["message"]["text"] = message.content

        if message.quick_replies:
            payload["message"]["quick_replies"] = [x.to_dict() for x in message.quick_replies]

        if message.metadata:
            payload["message"]["metadata"] = message.metadata

        if message.tag:
            payload["tag"] = message.tag

        print(payload)
        self.send_raw(payload)

    def typing_on(self, user_id):
        if isinstance(user_id, User):
            user_id = user_id.id

        payload = {
            "recipient" : {
                "id": user_id
            },
            "sender_action": "typing_on"
        }
        self.send_raw(payload)

    def typing_off(self, user_id):
        if isinstance(user_id, User):
            user_id = user_id.id

        payload = {
            "recipient": {
                "id": user_id
            },
            "sender_action": "typing_off"
        }
        self.send_raw(payload)

    def mark_seen(self, user_id):
        if isinstance(user_id, User):
            user_id = user_id.id

        payload = {
            "recipient": {
                "id": user_id
            },
            "sender_action": "mark_seen"
        }
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
