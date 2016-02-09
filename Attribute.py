class Attribute:
    def __init__(self, value):
        self.value = value

class MasterAttribute:
    def __init__(self, name, number, values):
        self.name = name
        self.number = number
        self.values = values #list of possible values attribute can have
