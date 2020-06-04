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

class Device(object):

  def __init__(self, deviceID, rest, mqtt="", resources):
    self.deviceID = deviceID
    self.end_points['rest'] = rest
    self.end_points['mqtt'] = mqtt
    self.resources = resources
    self.timestamp = datetime.datetime.now()

    # Store object in devices.json
    with open('../Database/devices.json', "w") as file:
      file.write(json.dumps(self)) 