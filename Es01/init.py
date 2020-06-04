# Documentazione ENDPOINT

# Devices
#
# GET
# - /devices                Retrieve all the registered devices
# - /devices/:deviceId      Retrieve a specific device with a deviceID
# POST
# - /devices/new            Add a new device


import cherrypy

class Catalog(object): 
  exposed = True
    
  def GET(self, *uri, **params):
    return open('./freeboard/index.html')

  def POST(self, *uri, **params):
    if uri[0]=="saveDashboard":
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