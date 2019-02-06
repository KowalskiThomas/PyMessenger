from classes import MessagingEntry


def parse_raw_data(data):
    chunks = list()
    for entry in data["entry"]:
        if "messaging" in entry:
            for messaging_entry in entry.get("messaging"):
                chunks.append(MessagingEntry.from_dict(messaging_entry))
            continue
        
        print(entry)

    return chunks
