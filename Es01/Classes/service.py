import json
# Classe per la gestione dei Devices
#
# Formato json:
# {
#   serviceID: "",
#   description: "",
#   end_points: {
#     rest: "",
#     mqtt: "",
#   },
#   timestamp: ""
# }

##
# Service object
##
class Service(object):
    
    def __init__(self, serviceID, description, rest, mqtt=""):
        self.deviceID = deviceID
        self.description = description
        self.end_points['rest'] = rest
        self.end_points['mqtt'] = mqtt
        self.timestamp = datetime.datetime.now()

##
# ServiceManager object
##
class ServiceManager(object):

  def __init__(self):
    self.services = []
    self.n = 0
    # Controllo json
    if os.path.exists('./Database/services.json'):
      with open('./Database/services.json') as file:
        self.services = json.load(file)
        self.n = len(self.services)

  # Add service
  def addService(self, description, rest, mqtt):
    serviceID = self.n
    service = Service(serviceID, description, rest, mqtt)
    self.services.append(service)
    self.n += 1

    # Store object in devices.json
    with open('../Database/services.json', "w") as file:
      file.write(json.dumps(self.services))

  # Get single device
  def getSingleService(self, serviceID):
    return json.dumps(self.services[serviceID])

  # Get all devices
  def getServices(self):
    return json.dumps(self.services)

  # Remove devices based on timestamp
  # def removeDevices(self, timestamp):