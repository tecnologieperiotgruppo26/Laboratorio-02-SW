# Classe per la gestione del MessageBroker
#
# Formato json:
# {
#   "ip": "",
#   "port": ""
# }

import datetime
import os
import json

##
# MessageBroker object
##
class MessageBroker(object):

  def __init__(self, ip, port):
    self.ip = ip
    self.port = port

    # Store object in mb.json
    with open('Database/mb.json', "w") as file:
      file.write(json.dumps(self))

  def getMessageBroker(self):
    return json.dumps(self)