##
# Client
#

import requests
import time

def getMessageBroker():
  r = requests.get('http://localhost:8080/messagebroker')
  print(r.text)


if __name__ == "__main__":
  deviceID=-1
  while True:
    print("Client is running")

    time.sleep(60)

    