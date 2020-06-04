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
import json

##
# Device object
##
class Device(object):

  def __init__(self, deviceID, rest, mqtt="", resources):
    self.deviceID = deviceID
    self.end_points['rest'] = rest
    self.end_points['mqtt'] = mqtt
    self.resources = resources
    self.timestamp = datetime.datetime.now()

##
# DeviceManager object
##
class DeviceManager(object):

  def __init__(self):
    self.devices=[]
    self.n=0

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
  # def removeDevices(self, timestamp):
