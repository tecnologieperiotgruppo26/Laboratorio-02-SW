# Documentazione ENDPOINT

# Message Broker
#
# GET
# - /messagebroker          Retrieve all the registered devices
# POST
# - /messagebroker/new      Add a new message broker
# 
#
# Devices
#
# GET
# - /devices                Retrieve all the registered devices
# - /devices/:deviceId      Retrieve a specific device with a deviceID
# POST
# - /devices/new            Add a new device
#
#
# Users
#
# GET
# - /users                Retrieve all the registered users
# - /users/:userID        Retrieve a specific user with a userID
# POST
# - /users/new            Add a new user


import cherrypy
import os
import datetime
from Classes.messagebroker import *
from Classes.device import *
from Classes.user import *
from Classes.service import *


def isIDvalid(string):
  try:
    int(string)
    return True
  except:
    return False
  
def isUriMultiple(uri):
  if len(uri) > 1:
    return True
  return False

class Catalog(object): 
  exposed = True

  def __init__(self):
    self.messageBroker = MessageBrokerManager()
    self.deviceManager = DeviceManager()
    self.userManager = UserManager()
    self.serviceManager = ServiceManager()

  def GET(self, *uri, **params):
    # Il metodo GET serve solo per la visualizzazione di infrmazioni del Catalog, per le aggiunte utilizzare POST
    # Questo flag mi indica se uri ha lunghezza maggiore di 1
    flag = isUriMultiple(uri)
    #errore qui sotto : IndexError: tuple index out of range, se faccio l'accesso a localhost ritora un 500
    if uri:
      if uri[0]=="messagebroker":
        return self.messageBroker.getMessageBroker()
      elif uri[0]=="devices" and flag:
        if isIDvalid(uri[1]): # deviceID
          if int(uri[1]) < self.deviceManager.getNumberOfDevices():
            return self.deviceManager.getSingleDevice(int(uri[1]))
          else:
            raise cherrypy.HTTPError(404, "Bad Request!")
        else:
          raise cherrypy.HTTPError(404, "Bad Request!")
      elif uri[0]=="devices":
        return self.deviceManager.getDevices()
      #GET USERS
      elif uri[0]=="users" and flag:
        if isIDvalid(uri[1]): # deviceID
          if int(uri[1]) < self.userManager.getNumberOfUsers():
            return self.userManager.getSingleUser(int(uri[1]))
          else:
            raise cherrypy.HTTPError(404, "Bad Request!")
        else:
          raise cherrypy.HTTPError(404, "Bad Request!")
      elif uri[0]=="users":
        return self.userManager.getUsers()
      #GET SERVICES
      elif uri[0]=="services" and flag:
        if isIDvalid(uri[1]): # deviceID
          if int(uri[1]) < self.serviceManager.getNumberOfServices():
            return self.serviceManager.getSingleService(uri[1])
          else:
            raise cherrypy.HTTPError(404, "Bad Request!")
        else:
          raise cherrypy.HTTPError(404, "Bad Request!")
      elif uri[0]=="services":
        return self.serviceManager.getServices()
    #else generico per "homepage"
    else:
      menu = "GET httpREST<br/>" \
             "<dl>/devices -> retrieve all the registered devices<br/>" \
             "<dl>/devices/[deviceId] -> retrieve a specific device<br/>" \
             "<dl>/users -> retrieve all the registered users<br/>" \
             "<dl>/users/:urserId -> retrieve a specific user<br/>"
      return "{}".format(menu)

  def POST(self, *uri, **params):
    # Il metodo POST accetta solo l'aggiunta di risorse al Catalog, per le informazioni si utilizza GET
    # Questo flag mi indica se uri ha lunghezza maggiore di 1
    flag = isUriMultiple(uri)
    if uri[0]=="messagebroker" and flag:
      if uri[1]=="new":
        self.messageBroker.addMessageBroker(params['ip'],params['port'])
      else:
        raise cherrypy.HTTPError(404, "Bad Request!")
    elif uri[0]=="devices" and flag:
      if uri[1]=="new":
        self.deviceManager.addDevice(time.time(), params['end_points']['rest'],params['resources'],params['end_points']['mqtt'])
      elif isIDvalid(uri[1]) and int(uri[1]) < self.serviceManager.getNumberOfServices():
        self.deviceManager.updateDevice(int(uri[1]), time.time())
      else:
        raise cherrypy.HTTPError(404, "Bad Request!")
        

if __name__ == '__main__': 
  conf = {
    '/': {
      'tools.sessions.on': True,
      'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
      'tools.staticdir.root': os.path.abspath(os.getcwd()) 
    }
  }
  cherrypy.tree.mount(Catalog(), '/', conf) 
  cherrypy.engine.start()
  #cherrypy.engine.block()
  input()
  Catalog().deviceManager.__del__()
  cherrypy.engine.stop()
  #Catalog().deviceManager.__del__()
