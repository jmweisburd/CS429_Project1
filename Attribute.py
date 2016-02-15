'''
The Attribute class represents the value of a particular attribute
Originally, I planned for it to be more in detailed but it turned out to just be
a character
The Entity class (mushrooms) are essentially just lists of these attributes
'''
class Attribute:
    def __init__(self, value):
        self.value = value

'''
A MasterAttribute instance holds all of the information about one particular
attribute. It holds the attribute name, the attribute number, the possible values
an attribute can have, and the degrees of freedom the attribute will have to look up
in the chi squared table
'''
class MasterAttribute:
    def __init__(self, name, number, values):
        self.name = name
        self.number = number
        self.values = values #list of possible values attribute can have
        self.dof = len(self.values) - 1
