##
# Client
#

import requests

def getMessageBroker():
  r = requests.get('http://localhost:8080/messagebroker')
  print(r.text)

def getAllDevices():
  r = requests.get('http://localhost:8080/devices')
  print(r.text)

def getSingleDevice(deviceID):
  r = requests.get(f"http://localhost:8080/devices/{deviceID}")
  print(r.text)

def getAllUsers():
  r = requests.get('http://localhost:8080/users')
  print(r.text)

def getSingleUser(userID):
  r = requests.get(f"http://localhost:8080/users/{userID}")
  print(r.text)
  
def getAllServices():
  r = requests.get('http://localhost:8080/services')
  print(r.text)

def getSingleService(userID):
  r = requests.get(f"http://localhost:8080/services/{serviceID}")
  print(r.text)

if __name__ == "__main__":
  flag=0
  while (flag==0):
    print("Available options:")
    print("0 - Retrieve message broker")
    print("1 - Retrieve all registered devices")
    print("2 - Retrieve single device")
    print("3 - Retrieve all users")
    print("4 - Retrieve single user")
    print("5 - Retrieve all services")
    print("6 - Retrieve single service")
    print("7 - Exit")
    input_val = int(input("Enter command number: "))

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
      getAllServices()
    elif (input_val==6):
      serviceID=input("Enter service id: ")
      getSingleService(serviceID)
    elif (input_val==7):
      flag=1
    else:
      print("Wrong number!")

