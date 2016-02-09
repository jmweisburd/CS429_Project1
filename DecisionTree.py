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
    def __init__(self, parent_split_attribute, parent_split_value, e_subset, a_attributes):
        self.e_subset = e_subset #subset of the entities/mushrooms that made it to this node
        self.a_attributes = a_attributes #available attributes to split on
        
        self.parent_split_attribute = parent_split_attribute #what attribute the parent node split on
        self.parent_split_value = parent_split_value #what value the parent node split on
        
        self.total = len(e_subset) #how many entities this node has
        
        self.node_type = None #node_type: split, neg, or pos
        self.node_entropy = 0
        self.entropy_list = [] #list of entropies to split on
        
        self.attribute_to_split_on = None #if a split node, what attribute number to split on
        
        self.children = [] #list of child nodes
        self.num_neg = self.countNegatives(e_subset)
        self.num_pos = self.total - self.num_neg
        
        self.classifyNode()
        
        if self.node_type != "neg" and self.node_type != "pos":
            self.splitNode()


    #counts the negative entities in an entity list
    def countNegatives(self, entity_list):
        counter = 0
        for e in entity_list:
            if e.final_class == "n":
                counter += 1
    
        return counter
    
    #classifies the node as either neg, pos, or split
    def classifyNode(self):
        if self.num_neg == self.total:
            self.node_type = "neg"
        elif self.num_pos == self.total:
            self.node_type = "pos"
        else:
            self.node_type = "split"

    def splitNode(self):
        self.fillEntropyList()
        self.calculateNodeEntropy()
        self.calculateAttributeEntropy()
        self.findMaxGain()
        self.splitOnAttribute()

    #makes EntropyAccumulators for each attribute to use to calculate the max gain
    def fillEntropyList(self):
        for a in self.a_attributes:
            self.entropy_list.append(EntropyAccumulator(a.number))

    #calculates the entropy of the whole entity subset based on if the entities are pos or neg
    #does not calculate entropies for attributes
    def calculateNodeEntropy(self):
        self.node_entropy = (logEquation(self.num_pos, self.total) + logEquation(self.num_neg, self.total))

    #calculates the entropy of a particular value of a particular attribute
    def calculateAttributeEntropy(self):
        for a in self.a_attributes:
            a_number = a.number
            for value in a.values:
                #make a subset of entities at this node with a particular attribute value
                ents_with_value = self.makeValueSubset(a_number, value)
                
                subset_total = len(ents_with_value)
                subset_frac = float(subset_total)/self.total
                subset_neg = self.countNegatives(ents_with_value)
                subset_pos = subset_total - subset_neg
                
                subset_value_entropy = subset_frac*(logEquation(subset_pos, subset_total) + logEquation(subset_neg, subset_total))
                
                for entropy in self.entropy_list:
                    if entropy.attribute_number == a.number:
                        entropy.addEntropy(subset_value_entropy)
                        break

    #Finds all of the entities in a list with a particular attribute value
    def makeValueSubset(self, a_number, value):
        ents_with_value = []
        for e in self.e_subset:
            if e.attributeList[a_number].value == value:
                ents_with_value.append(e)

        return ents_with_value

    #finds the max information gain at a node after finding all the entropies for each attribute
    def findMaxGain(self):
        gain = 0
        attribute = None
        for ent in self.entropy_list:
            test = self.node_entropy - ent.entropy
            if test > gain:
                gain = test
                attribute = ent.attribute_number

        self.attribute_to_split_on = attribute

    def splitOnAttribute(self):
        get_attribute = None
        entity_subset = []
        for a in self.a_attributes:
            if a.number == self.attribute_to_split_on:
                get_attribute = a
                break
    
        attributes_to_pass_on = copy.deepcopy(self.a_attributes)
        for a in attributes_to_pass_on:
            if a.number == self.attribute_to_split_on:
                attributes_to_pass_on.remove(a)
        
        for value in get_attribute.values:
            entity_subset = []
            entity_subset = self.makeValueSubset(get_attribute.number, value)
            self.children.append(Node(get_attribute.number, value, entity_subset, attributes_to_pass_on))


class EntropyAccumulator:
    def __init__(self, attribute_number):
        self.attribute_number = attribute_number
        self.entropy = 0

    def addEntropy(self, entropy):
        self.entropy += entropy











