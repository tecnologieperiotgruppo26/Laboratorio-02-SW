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
    if (deviceID==-1):
      payload = {'resources': ['temp'],'rest':'','mqtt':''}
      r = requests.post('http://localhost:8080/devices/new', data=payload)
      deviceID = int(r.text)
      print(f"deviceID: {deviceID}")
    else:
      r = requests.post(f"http://localhost:8080/devices/{deviceID}")
      print("Device updated!")
    time.sleep(20)

    