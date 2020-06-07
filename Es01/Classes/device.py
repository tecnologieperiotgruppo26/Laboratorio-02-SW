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

  def toDict(self):
    dict = {"deviceID" : "{}".format(self.deviceID),
            "end_points": {"rest" : "{}".format(self.end_points["rest"]),
                           "mqtt" : "{}".format(self.end_points["mqtt"])
                          },
            "resources" : "{}".format(self.resources),
            "timestamp" : "{}".format(self.timestamp)
            }
    return dict

  def toString(self):
    return "{}".format(self.toDict())

##
# DeviceManager object
##
class DeviceManager(object):

  # Tempo in minuti prima dell'eleminazione se il timestamp non viene aggiornato
  TIMEOUT = 24*60   #prova, da reimpostare a 2
  tmp=[]

  def __init__(self):
    self.devices = []
    self.n = 0
    # Controllo json
    if os.path.exists('Database/devices.json'):
      with open('Database/devices.json') as f:
        tmp = dict(json.loads(f.read()))['devices']
        for obj in tmp:
          self.devices.append(Device(obj['deviceID'],obj['timestamp'],obj['resources'],obj['end_points']['rest'],obj['end_points']['mqtt']))
        # Mantiene consistenza nella numerazione degli elementi
        if len(self.devices):
          self.n = int(self.devices[-1].getDeviceID()) + 1

    # Thread
    self.lock = threading.Lock()
    #qui inserisco il flag stop_thread, aggiunto come campo per bloccare il while true del thread,
    #altrimenti ho paura che essendo sempre "impegnato" non rientrerà mai nella join
    #perchè dovrebbe rientrare solo alla fine della sua run. che con il while true non termina mai
    self.thread = threading.Thread(target=self.removeDevices) #, args =(lambda : stop_thread, )
    self.thread.start()
    """
    facendo partire subito il thread rimuove tutti i devices
    """

  # Stop Execution
  def __del__(self):     #questa era la __DEL__, perchè è stato fatto un override?
    self.thread.join(1)
    self.lock.acquire()
    print("Sono nella finish")
    print(f"{self.devices}")
    with open('Database/devices.json', "w") as file:
      json.dump(self.getDevicesForJSon(), file)   #c'era la self.devices
    self.lock.release()

  # Add device
  def addDevice(self, timestamp, rest, resources, mqtt=""):
    deviceID = self.n
    device = Device(deviceID, timestamp, rest, resources, mqtt=mqtt)
    self.devices.append(device)
    self.n += 1

    # Store object in devices.json
    self.lock.acquire()
    print("Sono nella addDevices")
    with open('Database/devices.json', "w") as file:
      json.dump(self.getDevicesForJSon(), file)#      json.dump(self.devices, file)
    self.lock.release()

  # Get single device
  def getSingleDevice(self, deviceID):
    print("Sono nella getSingleDevices")
    for device in self.devices:
      if device.getDeviceID() == deviceID:
        return json.dumps(device)
    else:
      return "{}"

  # Get all devices
  def getDevices(self):
    return json.dumps(self.devices)

  def getDevicesForJSon(self):
    listOfDevicesAsDicts = []
    for device in self.devices:
      listOfDevicesAsDicts.append(device.toDict())
    dict = {"devices" : listOfDevicesAsDicts}
    return dict

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
      print("Sono nella removeDevices")
      if os.path.exists('Database/devices.json'):
        with open('Database/devices.json', "w") as file:
          json.dump(self.getDevicesForJSon(), file)#      json.dump(self.devices, file)
      self.lock.release()
      time.sleep(self.TIMEOUT)#perchè dorme per timeout?

  # Update an existin device
  def updateDevice(self, deviceID, timestamp): # per altre info basta aggiungere altri argomenti al metodo
    for device in self.devices:
      if device.getDeviceID() == deviceID:
        device.updateAtrr(timestamp)
    else:
      # Da definire come si vuole gestire, ma dal momento che siamo su mqtt penso si possa
      # lasciare al caso l'avvenuta conferma
      return 404

#File "C:\Users\emanu\Desktop\PoliTo\Semestre 4-2\IoT\Laboratorio\Laboratorio-02-SW\Es01\Classes\device.py", line 115, in removeDevices
#    json.dump(self.devices, file)
#File "C:\Users\emanu\AppData\Local\Programs\Python\Python38-32\lib\json\__init__.py", line 179, in dump
#   for chunk in iterable:
#raise TypeError(f'Object of type {o.__class__.__name__} '
#TypeError: Object of type Device is not JSON serializable