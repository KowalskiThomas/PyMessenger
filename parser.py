class Entry:
    def __init__(self, page_id, timestamp):
        self.page_id = page_id
        self.timestamp = timestamp

class Attachment:
    def __init__(self):
        self.type = None
        self.url = None

    @staticmethod
    def from_dict(d):
        x = Attachment()
        x.type = d["type"]
        x.url = d["payload"]["url"]

class MessagingEntry:
    def __init__(self):
        self.recipient = None
        self.sender = None
        self.timestamp = None
        self.message = None
        self.mid = None
        self.text = None
        self.quick_reply_payload = None
        self.attachments = None

    @staticmethod
    def from_dict(d):
        x = MessagingEntry()
        x.sender = d["sender"]["id"]
        x.recipient = d["recipient"]["id"]
        x.timestamp = d["timestamp"]
        x.message = d["message"]["text"]
        x.mid = d["message"]["mid"]
        x.quick_reply_payload = d["message"].get("quick_reply", dict()).get("payload", None)
        x.attachments = [Attachment.from_dict(y) for y in d.get("attachments", list())]

        return x

def parse_raw_data(data):
    chunks = list()
    for entry in data["entry"]:
        if "messaging" in entry:
            for messaging_entry in entry.get("messaging"):
                chunks.append(MessagingEntry.from_dict(messaging_entry))
            continue
        
        print(entry)

    return chunks
