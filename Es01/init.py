# Documentazione ENDPOINT

# Devices
#
# GET
# - /devices                Retrieve all the registered devices
# - /devices/:deviceId      Retrieve a specific device with a deviceID
# POST
# - /devices/new            Add a new device


import cherrypy
import os
from Classes.device import *

class Catalog(object): 
  exposed = True

  def __init__(self):
    self.deviceManager = DeviceManager()

  def GET(self, *uri, **params):
    if uri[0]=="devices":
      return self.deviceManager.getDevices()

  def POST(self, *uri, **params):
    if uri[0]=="devices":
      if uri[1]=="new":
        print("ok")
      # with open('./freeboard/static/dashboard/dashboard.json', "w") as file:
      #   print(f"{params['json_string']}")
      #   file.write(params['json_string'])

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