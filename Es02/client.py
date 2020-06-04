##
# Client
#

import requests

def getMessageBroker(self):
  r = requests.get('http://localhost:8080/messagebroker')
  print(r.json)

def getAllDevices(self):
  r = requests.get('http://localhost:8080/devices')
  print(r.json)

def getSingleDevice(self, deviceID):
  r = requests.get(f"http://localhost:8080/devices/{deviceID}")
  print(r.json)

def getAllUsers(self):
  r = requests.get('http://localhost:8080/users')
  print(r.json)

def getSingleUser(self, userID):
  r = requests.get(f"http://localhost:8080/users/{deviceID}")
  print(r.json)

if __name__ == "__main__":
  flag=0
  while (flag==0):
    print("Available options:")
    print("0 - Retrieve message broker")
    print("1 - Retrieve all registered devices")
    print("2 - Retrieve single device")
    print("3 - Retrieve all users")
    print("4 - Retrieve single user")
    print("5 - Exit")
    input_val = input("Enter command number: ")

    if (input_val==0):
      getMessageBroker()
    elif (input_val==1):
      getAllDevices()
    elif (input_val==2):
      deviceID=input("Enter device id: ")
      getSingleDevice(deviceID)
    elif (input_val==3):
      getAllUsers()
    elif (input_val==4):
      userID=input("Enter user id: ")
      getSingleUser(userID)
    elif (input_val==5):
      flag=1
    else:
      print("Wrong number!")

