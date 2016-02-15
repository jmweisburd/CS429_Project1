from Entity import *
from math import *
import copy

def logEquation(num, den):
    if num == 0:
        return 0
    else:
        a = float(num)/den
        return -(a)*(log(a,2))

def chiSquaredValue(r_pos, e_pos, r_neg, e_neg):
    if e_pos == 0:
        p_term = 0
    else:
        p_term = (float(pow((r_pos-e_pos),2))/e_pos)

    if e_neg == 0:
        n_term = 0
    else:
        n_term = (float(pow((r_neg-e_neg),2))/e_neg)

    return p_term + n_term

class DecisionTree:
    def __init__(self, title, training_list, testing_list, all_attributes, chi_squared_table, confidence, splitting_on_entropy):
        self.root = Node(None, None, training_list, all_attributes, splitting_on_entropy, 0)
        self.title = title
        self.all_attributes = all_attributes
        self.chi_squared_table = chi_squared_table
        self.confidence = confidence
        self.accuracy = 0
        self.testing_list = testing_list
        self.pruneTree(self.root)
        self.measureAccuracy()

    def classifyEntity(self, entity):
        current = self.root
        final_type = None
        while current.node_type == "split":
            node_split = current.attribute_to_split_on
            for n in current.children:
                if entity.attributeList[node_split].value == n.parent_split_value:
                    current = n

        final_type = current.node_type
        if final_type == "pos":
            return "e"
        else:
            return "p"

    def pruneTree(self, node):
        if node.node_type != "split":
            return
        else:
            self.pruneNode(node)
            for n in node.children:
                self.pruneTree(n)


    def rootVisit(self):
        root_child = self.root.children[6]
        root_child_2 = root_child.children[7]
        root_child_3 = root_child_2.children[1]
        root_child_4 = root_child_2.children[6]
        for n in root_child_3.children:
            print n.node_type

    def visitAllNodes(self, node):
        if len(node.children) == 0:
            #print node.node_type
            return
        else:
            #print node.node_type, " ", node.attribute_to_split_on
            for n in node.children:
                self.visitAllNodes(n)

    def calculateChiValueOfNode(self, node):
        total = node.total
        neg = node.num_neg
        pos = node.num_pos
        total_chi_value = 0
        for child in node.children:
            c_total = child.total
            c_pos = child.num_pos
            c_neg = child.num_neg
            e_pos = (pos)*(c_pos+c_neg)/total
            e_neg = (neg)*(c_pos+c_neg)/total
            total_chi_value += chiSquaredValue(c_pos, e_pos, c_neg, e_neg)
        return total_chi_value

    def pruneNode(self, node):
        dof = self.all_attributes[node.attribute_to_split_on].dof
        if self.confidence == 0:
            return
        else:
            chi_value = self.calculateChiValueOfNode(node)
            chi_look_up = self.chi_squared_table.lookup(dof, self.confidence)
            if chi_value <= chi_look_up:
                node.consolidateNode()

    def measureAccuracy(self):
        wrong = 0
        total = len(self.testing_list)
        for ent in self.testing_list:
            test = self.classifyEntity(ent)
            if test != ent.final_class:
                wrong += 1

        right = total - wrong
        self.accuracy = float(right)/total
        print self.accuracy

    def validateSet(self, validation_list):
        for ent in validation_list:
            ent.final_class = self.classifyEntity(ent)


class Node:
    def __init__(self, parent_split_attribute, parent_split_value, e_subset, a_attributes, splitting_on_entropy, height):
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

        self.height = height + 1
        #print self.height

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
            if e.final_class == "p":
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
            self.children.append(Node(get_attribute.number, value, entity_subset, attributes_to_pass_on, self.splitting_on_entropy, self.height))

    def consolidateNode(self):
        self.children = []
        if self.num_pos > self.num_neg:
            self.node_type = "pos"
        else:
            self.node_type = "neg"


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
