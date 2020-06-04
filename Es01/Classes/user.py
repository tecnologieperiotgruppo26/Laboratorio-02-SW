# Classe per la gestione degli User
#
# Formato json:
# {
#   userID: "",
#   name: "",
#   surname: "",
#   email: ""
# }

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

##
# UserManager object
##
class UserManager(object):

  def __init__(self):
    self.users = []
    self.n = 0

  # Add user
  def addUser(self, userID, name, surname, email):
    userID = self.n
    user = User(userID, name, surname, email)
    self.users.append(user)
    self.n += 1

    # Store object in users.json
    with open('../Database/users.json', "w") as file:
      file.write(json.dumps(self.users))

    # Get single user
    def getSingleUser(self, userID):
        return json.dumps(self.users[userID])

    # Get all users
    def getUsers(self):
        return json.dumps(self.users)

    # Remove devices based on timestamp
    # def removeDevices(self, timestamp):
        
