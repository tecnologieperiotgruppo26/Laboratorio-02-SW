"""
La classe resource serve a identificare correttamente tramite dizionario
tutti i valori della di ciò che arduino legge. per la dashboard tornerà utile,
per ora serve solo per <mettere dentro roba>
QUESTA NON SERVE A UN CAZZO, MA CANCELLARE CON CURA

"""


class Resource:
    def __init__(self, res, v, unit):
        self.res = res #risorsa['res']
        self.v = v #risorsa['v']
        self.unit = unit #risorsa['unit']
        print("Sono nella init della resource")

    def toDict(self):
        res = {"res": "{}".format(self.res),
               "value": "{}".format(self.v),
               "unit": "{}".format(self.unit)
               }
        return "{}".format(res) #res

    def getRes(self):
        return self.res

    def getV(self):
        return self.v

    def getUnit(self):
        return self.unit

