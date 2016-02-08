from Attribute import *

class Entity:
    def __init__(self, string):
        self.final_class = None
        self.attributeList = []

        string = string.replace("\n","")
        string = string.replace(",","")

        for char in string:
            self.attributeList.append(Attribute(char))
        self.final_class = self.attributeList.pop(0).value
