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

class User():
    
    def __init__(self, userID, name, surname, email):
        self.userID = userID
        self.name = name
        self.surname = surname
        self.email = email

class UserManager(object):

  def __init__(self):
    self.users = []
    self.n = 0

  def addUser(self, userID, name, surname, email):
    user = User(userID, name, surname, email)
    self.users.append(user)
    self.n += 1
        
