from Entity import *
from math import *
import copy

#helper function which calculates the log terms in the entropy equation which eventually
#get summed up to calculate the entropy of a large subset of objects or the entropy of
#a subset of objects with a particular attribute value
def logEquation(num, den):
    if num == 0:
        return 0
    else:
        a = float(num)/den
        return -(a)*(log(a,2))

#helper function to calculate the statistic which will be compared to chi square
#values
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

'''
The DecisionTree class is the class responsible for representing a decision tree.
It is essentially a root node with pointers to child nodes which have pointers to their child nodes
and so on until the tree culminates in leaves. These leaf nodes are the final classification of an object.
In this case, if a mushroom find its way to a leaf node, the leaf node will determine
if the mushroom is edible or not. The DecisionTree class also contains some helper functions.
In particular, when given a set of objects which the user knows the final classification type,
the DecisionTree class can calculate its accuracy from that set.
'''
class DecisionTree:
    #
    def __init__(self, title, training_list, testing_list, all_attributes, chi_squared_table, confidence, splitting_on_entropy):
        self.root = Node(None, None, training_list, all_attributes, splitting_on_entropy, 0)
        self.title = title #title of the tree
        self.all_attributes = all_attributes #all possible attributes to split on
        self.testing_list = testing_list
        self.chi_squared_table = chi_squared_table #chi squared table to look up values for pruning
        self.confidence = confidence  #confidence we want to prune the tree to
        self.accuracy = 0 #accuracy of the tree. calculated from a testing set

        self.pruneTree(self.root) #function to prune the tree
        self.measureAccuracy() #function to measure the accuracy of the tree

    #function to classify an object/entity as either edible or poisonious
    #input: entity to classify
    #output: "e" or "p"
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

    #Simple recursive function which makes its way down the tree and tries to pruneNode
    #any unessary/random splits
    def pruneTree(self, node):
        if node.node_type != "split":
            return
        else:
            self.pruneNode(node)
            for n in node.children:
                self.pruneTree(n)


    #Not a function to be used. Just a function to help me better understand the tree
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

    #Calculates the chi-square statistic of a node which splits at a particular attribute
    #Does this based on the expected counts and the real counts of the "p" and "e"
    #mushrooms after the split
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

    #Sees if a node which splits at a particular attribute really gives us a usefull
    #split based on the chi-squared test. If the calculated statistic is less than the
    #corresponding chi-squared value, then this function will consolidate the node information
    #a leaf node
    def pruneNode(self, node):
        dof = self.all_attributes[node.attribute_to_split_on].dof
        if self.confidence == 0:
            return
        else:
            chi_value = self.calculateChiValueOfNode(node)
            chi_look_up = self.chi_squared_table.lookup(dof, self.confidence)
            if chi_value <= chi_look_up:
                node.consolidateNode()

    #function which measures the accuracy of a this tree
    #takes a testing set to classify
    #compares the tree's classification of the testing set to the testing set's
    #true values
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

    #function which takes in a list of objects to classify
    #classifys each entity in the list as either "p" or "e"
    def validateSet(self, validation_list):
        for ent in validation_list:
            ent.final_class = self.classifyEntity(ent)


class Node:
    def __init__(self, parent_split_attribute, parent_split_value, e_subset, a_attributes, splitting_on_entropy):
        self.e_subset = e_subset #subset of the entities/mushrooms that made it to this node
        self.a_attributes = a_attributes #available attributes to split on
        self.splitting_on_entropy = splitting_on_entropy #boolean, are we splitting on entropy or CE?

        self.parent_split_attribute = parent_split_attribute #what attribute the parent node split on
        self.parent_split_value = parent_split_value #what value the parent node split on

        self.total = len(e_subset) #how many entities this node has

        self.node_type = None #node_type: split, neg, or pos

        self.node_entropy = 0 #entropy of the entity subset which made it to the node
        self.node_class_error = 0 #class error of the entity subset which made it to this node

        self.entropy_list = [] #list of entropies to split on
        self.class_error_list = [] #list of class errors to split on


        self.attribute_to_split_on = None #if a split node, what attribute number to split on

        self.children = [] #list of child nodes
        self.num_neg = self.countNegatives(e_subset) #count the negatives
        self.num_pos = self.total - self.num_neg #calculate the positives

        self.classifyNode() #classify the node as either "split", "pos", or "neg"

        #if the node is a "split" type node, split the node based on the requested heuristic
        #(see splitting_on_entropy boolean value)
        if self.node_type != "neg" and self.node_type != "pos":
            if self.splitting_on_entropy:
                self.splitNodeEntropy()
            else:
                self.splitNodeClassError()


    #counts the negative entities in an entity list
    #input: a list of entities
    #output: number of negatives ("p" mushrooms) in the list
    def countNegatives(self, entity_list):
        counter = 0
        for e in entity_list:
            if e.final_class == "p":
                counter += 1

        return counter

    #classifies the node as either "neg", "pos", or "split"
    #based on the number of "p" (neg), "e" (pos) mushrooms in the subset at this node
    def classifyNode(self):
        #if split on a missing attribute, or no more attributes are availabe to
        #split on, classify the node based on a majority count
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

    #helper function which splits the node based on the entropy heuristic
    def splitNodeEntropy(self):
        self.fillEntropyList()
        self.calculateNodeEntropy()
        self.calculateAttributeEntropy()
        self.findMaxGainEntropy()
        self.splitOnAttribute()

    #helper function which splits the node based on the class error heuristic
    def splitNodeClassError(self):
        print "splitting on class error"
        self.fillClassErrorList()
        self.calculateNodeClassError()
        self.calculateAttributeClassError()
        self.findMaxGainClassError()
        self.splitOnAttribute()

    #makes EntropyAccumulators for each available attribute to use to calculate the max gain
    #The attribute with the maximum gain will split the node
    def fillEntropyList(self):
        for a in self.a_attributes:
            self.entropy_list.append(EntropyAccumulator(a.number))

    #makes CEaccumulator for each available attribute to use to calculate the attribute
    #which will have the maximum class error
    #we will split on the attribute which has the maximum class error
    def fillClassErrorList(self):
        for a in self.a_attributes:
            self.class_error_list.append(CEaccumulator(a.number))

    #function to calculate the class error of the subset at the node
    def calculateNodeClassError(self):
        frac_neg = float(self.num_neg)/self.total
        frac_pos = float(self.num_pos)/self.total
        self.node_class_error = 1 - max(frac_neg,frac_pos)

    #function to calculate the class errors for all of the attributes which a node
    #can split on
    def calculateAttributeClassError(self):
        for a in self.a_attributes:
            a_number = a.number
            for value in a.values:
                #find all entities with a particular value for a possible attribute to split on
                ents_with_value = self.makeValueSubset(a_number, value)

                subset_total = len(ents_with_value)
                frac_max = 0
                #if no entities with value, that doesn't contribute to total class error of attribute
                if subset_total == 0:
                    frac_max = 0
                else:
                    #calculate the class error of the value of a particular attribute
                    subset_neg = self.countNegatives(ents_with_value)
                    subset_pos = subset_total - subset_neg
                    frac_neg = float(subset_neg)/subset_total
                    frac_pos = float(subset_pos)/subset_total
                    frac_max = max(frac_neg, frac_pos)
                    frac_max = 1 - frac_max
                    frac_max = (frac_max)*(float(subset_total)/self.total)

                #add all fo the class errors for the values of an attribute together
                for cerror in self.class_error_list:
                    if cerror.attribute_number == a_number:
                        cerror.addClassError(frac_max)
                        break


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
    #input: an attribute and attribute value of requested entities
    #output: a subset of all of the entities with requested attribute value
    def makeValueSubset(self, a_number, value):
        ents_with_value = []
        for e in self.e_subset:
            if e.attributeList[a_number].value == value:
                ents_with_value.append(e)

        return ents_with_value

    #finds which attribute will provide the highest information error for splitting
    def findMaxGainEntropy(self):
        gain = 0
        attribute = None
        for ent in self.entropy_list:
            test = self.node_entropy - ent.entropy
            if test > gain:
                gain = test
                attribute = ent.attribute_number

        self.attribute_to_split_on = attribute

    #finds which attribute will maximize the class error for splitting
    def findMaxGainClassError(self):
        gain = 0
        attribute = None
        for cerror in self.class_error_list:
            test = self.node_class_error - cerror.class_error
            if test > gain:
                gain = test
                attribute = cerror.attribute_number

        self.attribute_to_split_on = attribute

    #function which splits apart the subset of entities at a node into nodes of smaller subset_pos
    #which have been split on a particular attribute
    def splitOnAttribute(self):
        get_attribute = None
        entity_subset = []
        for a in self.a_attributes:
            if a.number == self.attribute_to_split_on:
                get_attribute = a
                break

        #remove the attribute we're splitting on from the available attributes to split on list
        attributes_to_pass_on = copy.deepcopy(self.a_attributes)
        for a in attributes_to_pass_on:
            if a.number == self.attribute_to_split_on:
                attributes_to_pass_on.remove(a)

        #for each value in the possible values of the attribute we're splitting on
        #make a new node with the entities which have those particular values
        for value in get_attribute.values:
            entity_subset = []
            entity_subset = self.makeValueSubset(get_attribute.number, value)
            self.children.append(Node(get_attribute.number, value, entity_subset, attributes_to_pass_on, self.splitting_on_entropy))

    #simple function used for pruning
    #if a decision is not statistically valid, consolidates the node into a "pos" or "neg"
    #node based on the majority of the entities in the node's entity list
    def consolidateNode(self):
        self.children = [] #empties children list
        if self.num_pos > self.num_neg:
            self.node_type = "pos"
        else:
            self.node_type = "neg"

#A simple helper class which just helps to associate two things together:
#An attribute and the calculated entropy for all possible values of that attribute
class EntropyAccumulator:
    def __init__(self, attribute_number):
        self.attribute_number = attribute_number
        self.entropy = 0

    def addEntropy(self, entropy):
        self.entropy += entropy

#A simple helper class which just helps to associate two things together:
#an attribute and the calculated class error for all possible values of that attribute
class CEaccumulator:
    def __init__(self, attribute_number):
        self.attribute_number = attribute_number
        self.class_error = 0

    def addClassError(self, class_error):
        self.class_error += class_error
