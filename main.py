from DatasetBuilder import *
from DecisionTree import *
import copy

data = Datasets()
data.readTraining()


possible_attributes_select = [MasterAttribute("outlook", 0, ["s","o","r"]), MasterAttribute("temperature", 1, ["h","m","c"]), MasterAttribute("humidity", 2, ["h","n"]), MasterAttribute("wind",3,["w","s"])]
master_attribute_list = copy.deepcopy(possible_attributes_select)

def attribute_dictionary(number):
    return {
        0: "outlook",
        1: "temperature",
        2: "humidity",
        3: "wind"
    }[number]

root = Node(None, data.training, possible_attributes_select)
