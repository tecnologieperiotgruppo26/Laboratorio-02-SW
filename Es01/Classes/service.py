# Classe per la gestione dei services
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

import datetime
import os
import json
import threading
import time

##
# Service object
##
class Service(object):
    
  def __init__(self, serviceID, timestamp, description, rest="", mqtt=""):
    self.serviceID = serviceID
    self.description = description
    self.end_points = {"rest": rest, "mqtt": mqtt}
    self.timestamp = timestamp
    
  def getServiceID(self):
    return self.serviceID

  def getTimestamp(self):
    return self.timestamp
  
  def toDict(self):
    dict = {"serviceID" : "{}".format(self.serviceID),
            "end_points": {"rest" : "{}".format(self.end_points["rest"]),
                           "mqtt" : "{}".format(self.end_points["mqtt"])
                          },
            "description" : "{}".format(self.description),
            "timestamp" : "{}".format(self.timestamp)
            }
    return dict

  def toString(self):
    return "{}".format(self.toDict())

##
# ServiceManager object
##
class ServiceManager(object):

  TIMEOUT = 60*60
  tmp = []
  
  def __init__(self):
    self.services = []
    self.n = 0
    # Controllo json
    if os.path.exists('Database/services.json'):
      with open('Database/services.json') as f:
        tmp = dict(json.loads(f.read()))['services']
        for obj in tmp:
          self.services.append(Device(obj['serviceID'],obj['timestamp'],obj['description'],obj['end_points']['rest'],obj['end_points']['mqtt']))
        # Mantiene consistenza nella numerazione degli elementi
        if len(self.services):
          self.n = int(self.services[-1].getServiceID()) + 1

  # Thread 
  self.lock = threading.Lock()
  self.thread = threading.Thread(target=self.removeServices)
  self.thread.start()
  
  # Stop Execution
  def __del__(self):
    self.thread.join(1)
    self.lock.acquire()
    print(f"{self.getServicesForJSon()}")
    with open('Database/services.json', "w") as file:
      json.dump(self.getServicesForJSon(), file)
    self.lock.release()
    
  # Add service
  def addDevice(self, timestamp, description, rest="", mqtt=""):
    serviceID = self.n
    service = Service(serviceID, timestamp, description, rest=rest, mqtt=mqtt)
    self.services.append(service)
    self.n += 1

    # Store object in services.json
    self.lock.acquire()
    with open('Database/services.json', "w") as file:
      json.dump(self.getServicesForJSon(), file)
    self.lock.release()

  # Get single service
  def getSingleService(self, serviceID):
    for service in self.services:
      if int(sevice.getServiceID()) == serviceID:
        return json.dumps(service.toDict())      
    return "{}"

  # Get all services
  def getServices(self):
    return json.dumps(self.getServicesForJson())

  def getServicesForJson(self):
    listOfServicesAsDicts = []
    for service in self.services:
      listOfServicesAsDicts.append(service.toDict())
    dict = {"services" : listOfServicesAsDicts}
    return dict
  
  # Remove services based on timestamp
  def removeServices(self):
    while True:
      tmp = []
      # Vengono mantenute solo le risorse che non hanno fatto scadere TIMEOUT
      for service in self.services:
        if time.time() - float(service.getTimestamp()) < self.TIMEOUT:
          tmp.append(service)
      self.services = tmp

      self.lock.acquire()
      if os.path.exists('Database/services.json'):
        with open('Database/services.json', "w") as file:
          json.dump(self.getServicesForJSon(), file)
      self.lock.release()
      time.sleep(self.TIMEOUT)
  
  # Update an existing service
  def updateDevice(self, serviceID, timestamp):
    for service in self.services:
      if service.getDeviceID() == serviceID:
        service.updateAtrr(timestamp)
    else:
      return 404

  def getNumberOfServices(self):
    return int(self.n)