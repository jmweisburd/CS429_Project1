from Attribute import *

class Entity:
    def __init__(self, string, know_final_class):
        self.final_class = None
        self.attributeList = []

        string = string.replace("\n","")
        string = string.replace(",","")
        if know_final_class:
            self.final_class = string[0]
            l = list(string)
            l[0] = ""
            string = "".join(l)
            for char in string:
                self.attributeList.append(Attribute(char))
        else:
            for char in string:
                self.attributeList.append(Attribute(char))