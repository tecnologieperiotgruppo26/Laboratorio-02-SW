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

class Service(object):
    
    def __init__(self, serviceID, description, rest, mqtt=""):
        self.deviceID = deviceID
        self.description = description
        self.end_points['rest'] = rest
        self.end_points['mqtt'] = mqtt
        self.timestamp = datetime.datetime.now()
        
        # Store object in services.json
        with open('../Database/services.json', "w") as file:
            file.write(json.dumps(self))