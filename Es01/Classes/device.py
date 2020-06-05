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

  def __init__(self, deviceID, timestamp, resources, rest="", mqtt=""):
    self.deviceID = deviceID
    self.end_points = {"rest": rest, "mqtt": mqtt}
    self.resources = resources
    self.timestamp = timestamp

  def updateAtrr(self,timestamp):
    self.timestamp = timestamp

  def getDeviceID(self):
    return self.deviceID

  def getTimestamp(self):
    return self.timestamp

##
# DeviceManager object
##
class DeviceManager(object):

  # Tempo in minuti prima dell'eleminazione se il timestamp non viene aggiornato
  TIMEOUT = 2*60
  tmp=[]

  def __init__(self):
    self.devices = []
    self.n = 0
    # Controllo json
    if os.path.exists('Database/devices.json'):
      with open('Database/devices.json') as f:
        #errore qui sotto :AttributeError: 'list' object has no attribute 'get'
        tmp = json.load(f).get('devices')
        for obj in tmp:
          self.devices.append(Device(obj['deviceID'],obj['timestamp'],obj['resources'],obj['end_points']['rest'],obj['end_points']['mqtt']))
        # Mantiene consistenza nella numerazione degli elementi
        if len(self.devices):
          self.n = int(self.devices[-1].getDeviceID()) + 1

    # Thread
    self.lock = threading.Lock()
    self.thread = threading.Thread(target=self.removeDevices)
    self.thread.start()

  # Stop Execution
  def __del__(self):
    self.thread.join()
    self.lock.acquire()
    with open('Database/devices.json', "w") as file:
      json.dump(self.devices, file)
    self.lock.release()

  # Add device
  def addDevice(self, timestamp, rest, resources, mqtt=""):
    deviceID = self.n
    device = Device(deviceID, timestamp, rest, resources, mqtt=mqtt)
    self.devices.append(device)
    self.n += 1

    # Store object in devices.json
    self.lock.acquire()
    with open('Database/devices.json', "w") as file:
      json.dump(self.devices, file)
    self.lock.release()

  # Get single device
  def getSingleDevice(self, deviceID):
    for device in self.devices:
      if device.getDeviceID() == deviceID:
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
        if time.time() - float(device.getTimestamp()) < self.TIMEOUT:
          tmp.append(device)
      self.devices = tmp

      self.lock.acquire()
      if os.path.exists('Database/devices.json'):
        with open('Database/devices.json', "w") as file:
          json.dump(self.devices, file)
      self.lock.release()
      time.sleep(self.TIMEOUT)

  # Update an existin device
  def updateDevice(self, deviceID, timestamp): # per altre info basta aggiungere altri argomenti al metodo
    for device in self.devices:
      if device.getDeviceID() == deviceID:
        device.updateAtrr(timestamp)
    else:
      # Da definire come si vuole gestire, ma dal momento che siamo su mqtt penso si possa
      # lasciare al caso l'avvenuta conferma
      return 404

