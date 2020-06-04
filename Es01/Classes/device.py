# Classe per la gestione dei Devices
#
# Formato json:
# {
#   deviceID: "",
#   end_points: {
#     rest: "",
#     mqtt: "",
#   },
#   resources: [],
#   timestamp: ""
# }

import datetime
import os
import json
import threading

##
# Device object
##
class Device(object):

  def __init__(self, deviceID, rest, resources, mqtt=""):
    self.deviceID = deviceID
    self.end_points['rest'] = rest
    self.end_points['mqtt'] = mqtt
    self.resources = resources
    self.timestamp = datetime.datetime.minute()
  
  def getDeviceID(self):
    return self.id
    
  def getTimestamp(self):
    return self.timestamp

##
# DeviceManager object
##
class DeviceManager(object):
  
  # Tempo in minuti prima dell'eleminazione se non il timestampo non viene aggiornato
  TIMEOUT = 2

  def __init__(self):
    self.devices = []
    self.n = 0
    # Controllo json
    if os.path.exists('./Database/devices.json'):
      with open('./Database/devices.json') as file:
        self.devices = json.load(file)
        # Non si può dare questo id perchè la lista potrebbe essere più corta dell'id al quale si era arrivati in precedenza
        self.n = len(self.devices)
    
    # Thread
    self.thread = threading.Thread(target=self.removeDevices)
    self.thread.start()

  # Add device
  def addDevice(self, rest, mqtt, resources):
    deviceID = self.n
    device = Device(deviceID, rest, mqtt, resources)
    self.devices.append(device)
    self.n += 1

    # Store object in devices.json
    with open('../Database/devices.json', "w") as file:
      file.write(json.dumps(self.devices))

  # Get single device
  def getSingleDevice(self, deviceID):
    return json.dumps(self.devices[deviceID])

  # Get all devices
  def getDevices(self):
    return json.dumps(self.devices)

  # Remove devices based on timestamp
  def removeDevices(self):
    while True:
      tmp = []
      for device in self.devices:
        if datetime.datetime.minute() - device.returnTimestamp < self.TIMEOUT:
          tmp.append(device)
      self.devices = tmp
      if os.path.exists('../Database/devices.json'):
        with open('../Database/devices.json', "w") as file:
          json.dump(self.devices)
        
    
