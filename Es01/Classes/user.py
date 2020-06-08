# Classe per la gestione degli User
#
# Formato json:
# {
#   userID: "",
#   name: "",
#   surname: "",
#   email: ""
# }

import datetime
import os
import json

##
# User object
##
class User():

  def __init__(self, userID, name, surname, email):
    self.userID = userID
    self.name = name
    self.surname = surname
    self.email = email

  def getUserID(self):
    return self.userID

  def getName(self):
    return self.name

  def getSurname(self):
    return self.surname

  def getEmail(self):
    return self.email

  def toDict(self):
    dict = {"userID": "{}".format(self.userID),
            "name": "{}".format(self.name),
            "surname": "{}".format(self.surname),
            "email": "{}".format(self.email)
            }
    return dict

  def toString(self):
    return "{}".format(self.toDict())

##
# UserManager object
##
class UserManager(object):

  def __init__(self):
    self.users = []
    self.n = 0

    if os.path.exists('Database/users.json'):
      with open('Database/devices.json') as f:
        tmp = dict(json.loads(f.read()))['users']
        for obj in tmp:
          self.users.append(User(obj['userID'],obj['name'],obj['surname'],obj['email']))
        # Mantiene consistenza nella numerazione degli elementi
        if len(self.users):
          self.n = int(self.users[-1].getUserID()) + 1
    else:
      with open('Database/users.json', "w") as f:
        f.write('{"users":[]}')

  # Add user
  def addUser(self, userID, name, surname, email):
    userID = self.n
    user = User(userID, name, surname, email)
    self.users.append(user)
    self.n += 1

    # Store object in users.json
    with open('Database/users.json', "w") as file:
      file.write(json.dumps(self.getUsersForJSon()))
    
    # Ritorno l'id per comunicarlo allo user che si è registrato
    return userID

  # Get single user
  def getSingleUser(self, userID):
    dict = self.users[userID].toDict()
    return json.dumps(dict)

  # Get all users
  def getUsers(self):
    return json.dumps(self.getUsersForJSon())

  def getUsersForJSon(self):
    listOfUsersAsDicts = []
    for Users in self.users:
      listOfUsersAsDicts.append(Users.toDict())
    dict = {"Users": listOfUsersAsDicts}
    return dict

  # Remove Users based on timestamp
  # def removeUsers(self, timestamp):
        
