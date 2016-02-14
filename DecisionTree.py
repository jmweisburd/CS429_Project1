from Entity import *
from math import *
import copy

def logEquation(num, den):
    if num == 0:
        return 0
    else:
        a = float(num)/den
        return -(a)*(log(a,2))

class DecisionTree:
    def __init__(self, entity_list, all_attributes, splitting_on_entropy):
       self.root = Node(None, None, entity_list, all_attributes, splitting_on_entropy)

    def classifyEntity(self, entity):
        current = self.root
        final_type = None
        while current.node_type == "split":
            node_split = current.attribute_to_split_on
            for n in current.children:
                if entity.attributeList[node_split].value == n.parent_split_value:
                    current = n

        final_type = current.node_type
        print final_type

class Node:
    def __init__(self, parent_split_attribute, parent_split_value, e_subset, a_attributes, splitting_on_entropy):
        self.e_subset = e_subset #subset of the entities/mushrooms that made it to this node
        self.a_attributes = a_attributes #available attributes to split on
        self.splitting_on_entropy = splitting_on_entropy #are we splitting on entropy or CE?
        
        self.parent_split_attribute = parent_split_attribute #what attribute the parent node split on
        self.parent_split_value = parent_split_value #what value the parent node split on
        
        self.total = len(e_subset) #how many entities this node has
        
        self.node_type = None #node_type: split, neg, or pos
        
        self.node_entropy = 0
        self.node_class_error = 0
        
        self.entropy_list = [] #list of entropies to split on
        self.class_error_list = []
        
        
        self.attribute_to_split_on = None #if a split node, what attribute number to split on
        
        self.children = [] #list of child nodes
        self.num_neg = self.countNegatives(e_subset)
        self.num_pos = self.total - self.num_neg
        
        self.classifyNode()
        
        if self.node_type != "neg" and self.node_type != "pos":
            if self.splitting_on_entropy:
                self.splitNodeEntropy()
            else:
                self.splitNodeClassError()


    #counts the negative entities in an entity list
    def countNegatives(self, entity_list):
        counter = 0
        for e in entity_list:
            if e.final_class == "n":
                counter += 1
    
        return counter
    
    #classifies the node as either neg, pos, or split
    def classifyNode(self):
        if len(self.a_attributes) == 0 or self.parent_split_value == "?":
            if self.num_neg >= self.num_pos:
                self.node_type = "neg"
            else:
                self.node_type = "pos"
        else:
            if self.num_neg == self.total:
                self.node_type = "neg"
            elif self.num_pos == self.total:
                    self.node_type = "pos"
            else:
                self.node_type = "split"

    def splitNodeEntropy(self):
        self.fillEntropyList()
        self.calculateNodeEntropy()
        self.calculateAttributeEntropy()
        self.findMaxGainEntropy()
        self.splitOnAttribute()
    
    def splitNodeClassError(self):
        self.fillClassErrorList()
        self.calculateNodeClassError()
        self.calculateAttributeClassError()
        self.findMaxGainClassError()
        self.splitOnAttribute()

    #makes EntropyAccumulators for each attribute to use to calculate the max gain
    def fillEntropyList(self):
        for a in self.a_attributes:
            self.entropy_list.append(EntropyAccumulator(a.number))

    def fillClassErrorList(self):
        for a in self.a_attributes:
            self.class_error_list.append(CEaccumulator(a.number))

    def calculateNodeClassError(self):
        frac_neg = float(self.num_neg)/self.total
        frac_pos = float(self.num_pos)/self.total
        self.node_class_error = 1 - max(frac_neg,frac_pos)
        
    def calculateAttributeClassError(self):
        for a in self.a_attributes:
            a_number = a.number
            for value in a.values:
                ents_with_value = self.makeValueSubset(a_number, value)
                
                subset_total = len(ents_with_value)
                frac_max = 0
                if subset_total == 0:
                    frac_max = 0
                else:
                    subset_neg = self.countNegatives(ents_with_value)
                    subset_pos = subset_total - subset_neg
                    frac_neg = float(subset_neg)/subset_total
                    frac_pos = float(subset_pos)/subset_total
                    frac_max = max(frac_neg, frac_pos)
                    frac_max = 1 - frac_max
                    frac_max = (frac_max)*(float(subset_total)/self.total)
                    
                for cerror in self.class_error_list:
                    if cerror.attribute_number == a_number:
                        cerror.addClassError(frac_max)


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
                
                if subset_total == 0:
                    subset_frac = 0
                else:
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
    def findMaxGainEntropy(self):
        gain = 0
        attribute = None
        for ent in self.entropy_list:
            test = self.node_entropy - ent.entropy
            if test > gain:
                gain = test
                attribute = ent.attribute_number

        self.attribute_to_split_on = attribute

    def findMaxGainClassError(self):
        gain = 0
        attribute = None
        for cerror in self.class_error_list:
            test = self.node_class_error - cerror.class_error
            if test > gain:
                gain = test
                attribute = cerror.attribute_number

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
            self.children.append(Node(get_attribute.number, value, entity_subset, attributes_to_pass_on, self.splitting_on_entropy))


class EntropyAccumulator:
    def __init__(self, attribute_number):
        self.attribute_number = attribute_number
        self.entropy = 0

    def addEntropy(self, entropy):
        self.entropy += entropy

class CEaccumulator:
    def __init__(self, attribute_number):
        self.attribute_number = attribute_number
        self.class_error = 0

    def addClassError(self, class_error):
        self.class_error += class_error





