# Documentazione ENDPOINT

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
# - /users                Retrieve all the registered devices
# - /users/:userID      Retrieve a specific device with a deviceID
# POST
# - /users/new            Add a new device


import cherrypy
import os
import datetime
from Classes.device import *
from Classes.user import *


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
    self.deviceManager = DeviceManager()
    self.userManager = UserManager()

  def GET(self, *uri, **params):
    # Il metodo GET serve solo per la visualizzazione di infrmazioni del Catalog, per le aggiunte utilizzare POST
    # Questo flag mi indica se uri ha lunghezza maggiore di 1
    flag = isUriMultiple(uri)
    #errore qui sotto : IndexError: tuple index out of range, se faccio l'accesso a localhost ritora un 500
    if uri[0]=="devices" and flag:
      if isIDvalid(uri[1]): # deviceID
        return self.deviceManager.getSingleDevice(int(uri[1]))
      else:
        raise cherrypy.HTTPError(404, "Bad Request!")
    elif uri[0]=="devices":
      return self.deviceManager.getDevices()
    elif uri[0]=="users":
      if uri[1]: # userID
        return self.userManager.getSingleUser(uri[1])
      else:
        return self.userManager.getUsers()
    #else generico per "homepage"
    else:
      menu = "GET httpREST\n" \
             "/devices -> retrieve all the registered devices\n" \
             "/devides/:deviceId -> retrieve a specific device\n" \
             "/users -> retrieve all the registered users\n" \
             "/users/:urserId -> retrieve a specific user\n"
      return menu

  def POST(self, *uri, **params):
    # Il metodo POST accetta solo l'aggiunta di risorse al Catalog, per le informazioni si utilizza GET
    # Questo flag mi indica se uri ha lunghezza maggiore di 1
    flag = isUriMultiple(uri)
    if uri[0]=="devices" and flag:
      if uri[1]=="new":
        self.deviceManager.addDevice(time.time(), params['end_points']['rest'],params['resources'],params['end_points']['mqtt'])
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
