from Attribute import *

'''
An Entity class is the representation of a mushroom/whatever object needs to be
classified in the decision tree. It holds a list of attribute values about its
cap-shape, color, odor. etc.
'''
class Entity:
    def __init__(self, string, know_final_class):
        self.final_class = None
        self.attributeList = []

        #replace all of the non attribute characters in the string read in from
        #the .txt data file
        string = string.replace("\n","")
        string = string.replace(",","")

        #if we know the final classification (the first character on the string)
        #remove it and store in the final_class data variable
        if know_final_class:
            self.final_class = string[0]
            l = list(string)
            l[0] = ""
            string = "".join(l)
            for char in string:
                #make attribues and add them to the entities attributeList
                self.attributeList.append(Attribute(char))
        else:
            #make attributes from string and add them to the entities attributeList
            for char in string:
                self.attributeList.append(Attribute(char))
