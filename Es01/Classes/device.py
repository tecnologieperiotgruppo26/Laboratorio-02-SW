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
import time

##
# Device object
##
class Device(object):

  def __init__(self, deviceID, timestamp, rest, resources, mqtt=""):
    self.deviceID = deviceID
    self.end_points['rest'] = rest
    self.end_points['mqtt'] = mqtt
    self.resources = resources
    self.timestamp = timestamp
  
  def updateAtrr(self,timestamp):
    self.timestamp = timestamp
  
  def getDeviceID(self):
    return self.id
    
  def getTimestamp(self):
    return self.timestamp

##
# DeviceManager object
##
class DeviceManager(object):
  
  # Tempo in minuti prima dell'eleminazione se il timestamp non viene aggiornato
  TIMEOUT = 2

  def __init__(self):
    self.devices = []
    self.n = 0
    # Controllo json
    if os.path.exists('../Database/devices.json'):
      with open('../Database/devices.json') as file:
        print(file.read())
        self.devices = json.load(file)
        print(self.devices)
        # Mantiene consistenza nella numerazione degli elementi
        if len(self.devices):
          self.n = self.devices[-1].returnDeviceID + 1
    
    # Thread
    self.lock = threading.Lock()
    self.thread = threading.Thread(target=self.removeDevices)
    self.thread.start()

  # Add device
  def addDevice(self, timestamp, rest, resources, mqtt=""):
    deviceID = self.n
    device = Device(deviceID, timestamp, rest, resources, mqtt=mqtt)
    self.devices.append(device)
    self.n += 1

    # Store object in devices.json
    self.lock.acquire()
    with open('../Database/devices.json', "w") as file:
      file.write(json.dumps(self.devices))
    self.lock.release()

  # Get single device
  def getSingleDevice(self, deviceID):
    for device in self.devices:
      if device.returnDeviceID == deviceID:
        return json.dumps(device)
    else:
      return "{}"

  # Get all devices
  def getDevices(self):
    return json.dumps(self.devices)

  # Remove devices based on timestamp
  def removeDevices(self):
    while True:
      tmp = []
      # Vengono mantenute solo le risorse che non hanno fatte scadere TIMEOUT
      for device in self.devices:
        if datetime.datetime.minute() - device.returnTimestamp.minute < self.TIMEOUT:
          tmp.append(device)
      self.devices = tmp
      
      self.lock.acquire()
      if os.path.exists('../Database/devices.json'):
        with open('../Database/devices.json', "w") as file:
          json.dump(self.devices)
      self.lock.release()
    time.sleep(self.TIMEOUT*60)

  # Update an existin device
  def updateDevice(self, deviceID, timestamp): # per altre info basta aggiungere altri argomenti al metodo
    for device in self.devices:
      if device.returnDeviceID == deviceID:
        device.updateAtrr(timestamp)
        return 200
    else:
      # Da definire come si vuole gestire
      return 404
  
# TESTING
if __name__ == "__main__":
  print(datetime.datetime.now().minute)