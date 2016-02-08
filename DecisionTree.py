from Entity import *
from math import log
import copy

def logEquation(num, den):
    if num == 0:
        return 0
    else:
        a = float(num)/den
        return -(a)*(log(a,2))

#class DecisionTree:
#   def __init__(self, entity_list, all_attributes):
#       root = Node(



class Node:
    def __init__(self, sub_attribute_split, e_subset, a_attributes):
        self.e_subset = e_subset
        self.a_attributes = a_attributes
        #self.a_attributes = copy.deepcopy(a_attributes) #available attributes
        self.sub_attribute_split = sub_attribute_split
        self.total = len(e_subset)
        self.num_pos = 0
        self.num_neg = 0
        self.node_type = None
        self.a_entropy = None
        self.node_entropy = 0
        self.entropy_list = []
        self.attribute_to_split_on = 0
        self.children = []
        
        self.countNegativesAndPositives()
        print "number negatives:", self.num_neg
        print "number positives:", self.num_pos
        self.classifyNode()
        if self.node_type != "no" and self.node_type != "yes":
            self.splitNode()
                    
    def splitNode(self):
        self.fillEntropyList()
        self.calculateNodeEntropy()
        self.calculateAttributeEntropy()
        self.findMaxGain()
        self.splitOnAttribute()

    def splitOnAttribute(self):
        get_attribute = None
        entity_subset = []
        for a in self.a_attributes:
            if a.number == self.attribute_to_split_on:
                get_attribute = a
                break
    
        #attributes_to_pass_on = copy.deepcopy(self.a_attributes)
        #for a in attributes_to_pass_on:
            #if a.number == self.attribute_to_split_on:
            #attributes_to_pass_on.remove(a)
        
        for sub_attribute in get_attribute.sub_attributes:
            print sub_attribute
            entity_subset = []
            entity_subset = self.makeSubattributeList(get_attribute.number, sub_attribute)
            self.children.append(Node(sub_attribute, entity_subset, self.a_attributes))


    def countNegativesAndPositives(self):
        for e in self.e_subset:
            if e.final_class == "n":
                self.num_neg += 1
            else:
                self.num_pos += 1

    def classifyNode(self):
        if self.num_neg == self.total:
            self.node_type = "no"
        elif self.num_pos == self.total:
            self.node_type = "yes"
        else:
            self.node_type = "split"

        print self.node_type

    def calculateNodeEntropy(self):
        self.node_entropy = (logEquation(self.num_pos, self.total) + logEquation(self.num_neg, self.total))
    
    def fillEntropyList(self):
        for a in self.a_attributes:
            self.entropy_list.append(EntropyAccumulator(a.number))
    
    def makeSubattributeList(self, a_number, sub_attribute):
        sub_attribute_list = []
        for e in self.e_subset:
            if e.attributeList[a_number].value == sub_attribute:
                sub_attribute_list.append(e)
        
        return sub_attribute_list
    
    def calculateNumberPositives(self, e_list):
        counter = 0
        for e in e_list:
            if e.final_class == "y":
                counter += 1
        return counter
                
    def findMaxGain(self):
        gain = 0
        attribute = None
        for ent in self.entropy_list:
            test = self.node_entropy - ent.entropy
            if test > gain:
                gain = test
                attribute = ent.attribute_number

        self.attribute_to_split_on = attribute
        print attribute
        print gain

    def calculateAttributeEntropy(self):
        for a in self.a_attributes:
            a_number = a.number
            for sub_attribute in a.sub_attributes:
                sub_attribute_list = self.makeSubattributeList(a_number, sub_attribute)
                sub_attribute_total = len(sub_attribute_list)
                sub_attribute_frac = float(sub_attribute_total)/self.total
                sub_attribute_pos = self.calculateNumberPositives(sub_attribute_list)
                sub_attribute_neg = sub_attribute_total - sub_attribute_pos
                sub_attribute_entropy = sub_attribute_frac*(logEquation(sub_attribute_pos, sub_attribute_total) + logEquation(sub_attribute_neg, sub_attribute_total))
                for ent in self.entropy_list:
                    if ent.attribute_number == a.number:
                        ent.addEntropy(sub_attribute_entropy)


class EntropyAccumulator:
    def __init__(self, attribute_number):
        self.attribute_number = attribute_number
        self.entropy = 0

    def addEntropy(self, entropy):
        self.entropy += entropy











