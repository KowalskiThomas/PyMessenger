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
    def __init__(self, content, content_type = ContentType.text, notification_type = NotificationType.regular, quick_replies = None):
        self.content = content
        self.content_type = content_type
        self.notification_type = notification_type
        self.quick_replies = quick_replies