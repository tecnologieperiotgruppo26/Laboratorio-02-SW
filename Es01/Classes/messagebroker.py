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

  def getMessageBroker(self):
    return json.dumps(self)

##
# MessageBroker object
##
class MessageBrokerManager(object):

  def __init__(self):
    self.messageBroker = {}
    if os.path.exists('Database/mb.json'):
      with open('Database/mb.json') as file:
        self.messageBroker = dict(json.loads(file.read()))

  # Add message broker
  def addMessageBroker(self, ip, port):
    if self.messageBroker!=False:
      self.messageBroker = MessageBroker(ip, port)
      # Store object in mb.json
      with open('Database/mb.json', "w") as file:
        json.dump(self.messageBroker, file)

  def getMessageBroker(self):
    return json.dumps(self.messageBroker)