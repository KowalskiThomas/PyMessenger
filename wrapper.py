import time

from example import Paybot

USER = 1
try:
    b = Paybot()
    while True:
        time.sleep(1)
    # while True:
    #     req = input("Bot1>")
    #     b.on_req(USER, req)
except KeyboardInterrupt:
    print()
except EOFError:
    print()