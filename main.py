from DatasetBuilder import *
from DecisionTree import *
import copy

data = Datasets()
data.readTraining()

possible_attributes_select = [MasterAttribute("cap-shape", 0, ["b", "c", "x", "f", "k", "s"]),
                              MasterAttribute("cap-surface", 1, ["f", "g", "y", "s"]),
                              MasterAttribute("cap-color", 2, ["n", "b", "c", "g", "r", "p", "u", "e", "w", "y"]),
                              MasterAttribute("bruises?", 3, ["t","f"]),
                              MasterAttribute("odor?", 4, ["a","l","c","y","f","m","n","p","s"]),
                              MasterAttribute("gill-attachment", 5, ["a","d","f","n"]),
                              MasterAttribute("gill-spacing", 6, ["c","w","d"]),
                              MasterAttribute("gill-size", 7, ["b","n"]),
                              MasterAttribute("gill-color", 8, [ "k", "n", "b", "h", "g", "r", "o", "p", "u", "e", "w", "y"]),
                              MasterAttribute("stalk-shape",9, ["e", "t"]),
                              MasterAttribute("stalk-root",10, ["b","c","u","e","z","r","?"]),
                              MasterAttribute("stalk-surface-above-ring", 11, ["f", "y", "k","s"]),
                              MasterAttribute("stalk-surface-below-ring", 12, ["f", "y", "k","s"]),
                              MasterAttribute("stalk-color-above-ring", 13, ["n", "b", "c", "g", "o", "p", "e", "w", "y"]),
                              MasterAttribute("stalk-color-below-ring", 14, ["n", "b", "c", "g", "o", "p", "e", "w", "y"]),
                              MasterAttribute("veil-type", 15, ["p", "u"]),
                              MasterAttribute("veil-color", 16, ["n","o","w","y"]),
                              MasterAttribute("ring-number", 17, ["n", "o", "t"]),
                              MasterAttribute("ring-type", 18, ["c", "e", "f", "l", "n", "p", "s", "z"]),
                              MasterAttribute("spore-print-color", 19, ["k", "n", "b", "h", "r", "o", "u", "w", "y" ]),
                              MasterAttribute("population", 20, ["a", "c", "n", "s", "v", "y"]),
                              MasterAttribute("habitat", 21, ["g", "l", "m", "p","u","w","d"])]

#master_attribute_list = copy.deepcopy(possible_attributes_select)

def attribute_dictionary(number):
    return {
        0: "outlook",
        1: "temperature",
        2: "humidity",
        3: "wind"
    }[number]


test_mushroom = Entity("f,y,g,f,f,f,c,b,g,e,b,k,k,n,n,p,w,o,l,h,v,d", False)

DT = DecisionTree(data.training, possible_attributes_select, True)

DT.classifyEntity(test_mushroom)

cs = ChiSquared()
cs.lookup(11, 99)