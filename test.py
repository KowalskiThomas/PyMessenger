import time
from server import Server

s = Server()
s.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("")