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
from Classes.device import *
from Classes.user import *

class Catalog(object): 
  exposed = True

  def __init__(self):
    self.deviceManager = DeviceManager()
    self.userManager = UserManager()

  def GET(self, *uri, **params):
    if uri[0]=="devices":
      if uri[1]: # deviceID
        return self.deviceManager.getSingleDevice(uri[1])
      else:
        return self.deviceManager.getDevices()
    elif uri[0]=="users":
      if uri[1]: # userID
        return self.userManager.getSingleUser(uri[1])
      else:
        return self.userManager.getUsers()

  def POST(self, *uri, **params):
    if uri[0]=="devices":
      if uri[1]=="new":
        self.deviceManager.addDevice(params['end_points']['rest'],params['end_points']['mqtt'],params['resources'])

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
  cherrypy.engine.block()