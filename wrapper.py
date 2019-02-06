import time

from example import Paybot

VERIFY_TOKEN = "mliqlmskdlqmskdlmqsclmkqsnfhqzopkdqlmskqsfjhqsufqlksjklqzlkdjqlksjdlqksjdliqzjpodqs"
ACCESS_TOKEN = "EAAExE9IwmSgBABZAsN9yCHd6zkBbusjootOK9tVz68kTZBjZC5hwSMmRqDCctvWuLqltZCnX7ZAQkG8AUpXmmYQF1p0ionuZCS4pVXuuUwdNtqAhojdNu62NTqmSTyjSS7KhGUFn5d0hlxLRpeQmT94N3fDH9AOZAeyiVRYlsnvem7A4kB0vins"
SERVER_URL = "https://158.ip-51-75-252.eu:5000"

USER = 1
try:
    b = Paybot(ACCESS_TOKEN)
    while True:
        time.sleep(1)
    # while True:
    #     req = input("Bot1>")
    #     b.on_req(USER, req)
except KeyboardInterrupt:
    print()
except EOFError:
    print()