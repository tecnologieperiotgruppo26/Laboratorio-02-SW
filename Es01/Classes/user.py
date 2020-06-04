import json

# Classe per la gestione degli User
#
# Formato json:
# {
#   userID: "",
#   name: "",
#   surname: "",
#   email: ""
# }

class User():
    
    def __init__(self, userID, name, surname, email):
        self.userID = userID
        self.name = name
        self.surname = surname
        self.email = email
        
        # Store object in users.json
        with open('../Database/users.json', "w") as file:
            file.write(json.dumps(self))
        
