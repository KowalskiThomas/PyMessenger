from enum import Enum


class NotificationType(Enum):
    regular = "REGULAR"
    silent_push = "SILENT_PUSH"
    no_push = "NO_PUSH"


class ContentType(Enum):
    location = "location"
    text = "text"
    phone_number = "user_phone_number"
    email = "user_email"


class MessagingTag(Enum):
    BUSINESS_PRODUCTIVITY = "BUSINESS_PRODUCTIVITY"
    COMMUNITY_ALERT = "COMMUNITY_ALERT"
    # TODO https://developers.facebook.com/docs/messenger-platform/send-messages/message-tags


class MessageType(Enum):
    Response = "RESPONSE"
    Update = "UPDATE"
    Message = "MESSAGE_TAG"


class Attachment:
    def __init__(self):
        self.type = None
        self.url = None

        # For locations
        self.lat = None
        self.long = None

        # For links
        self.title = None

    @staticmethod
    def from_dict(d: dict):
        x = Attachment()
        x.type = d["type"]

        if x.type == "fallback":
            x.url = d["url"]
            x.title = d["title"]
        else:
            x.url = d["payload"]["url"]
            if x.type == "location":
                x.lat = d["payload"]["coordinates"]["lat"]
                x.long = d["payload"]["coordinates"]["long"]
            elif x.type == "file" or x.type == "image" or x.type == "audio" or x.type == "video":
                # Nothing to do, we already have the URL
                pass

        return x

    def __repr__(self):
        return "Attachment ({type}), URL = {url}".format(
            type = self.type,
            url = self.url
        )


class MessagingEntry:
    def __init__(self):
        self.recipient:int = None
        self.sender = None
        self.timestamp = None
        self.message: str = None
        self.mid: str = None
        self.quick_reply_payload = None
        self.attachments = None
        self.continue_processing = True

    @staticmethod
    def from_dict(d):
        print("ENTRY", d)
        x = MessagingEntry()
        x.sender = d["sender"]["id"]
        x.recipient = d["recipient"]["id"]
        x.timestamp = d["timestamp"]
        x.message = d["message"].get("text", "")
        x.mid = d["message"]["mid"]
        x.quick_reply_payload = d["message"].get("quick_reply", dict()).get("payload", None)
        x.attachments = [Attachment.from_dict(y) for y in d["message"].get("attachments", list())]

        return x


class QuickReply:
    def __init__(self, title, payload, content_type = ContentType.text, image_url = None):
        self.title = title
        self.content_type = content_type
        self.image_url = image_url
        self.payload = payload

    def to_dict(self):
        return {
            "title": self.title,
            "content_type": self.content_type.value,
            "image_url": self.image_url,
            "payload": self.payload
        }


class Message:
    def __init__(self, content, content_type = ContentType.text, notification_type = NotificationType.regular, quick_replies = None, metadata = None, tag = None, message_type = MessageType.Response):
        self.content = content
        self.content_type = content_type
        self.notification_type = notification_type
        self.quick_replies = quick_replies
        self.metadata = metadata
        self.tag = tag
        self.message_type = message_type
