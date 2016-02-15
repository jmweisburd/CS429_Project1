from DatasetBuilder import *
from DecisionTree import *
import copy

data = Datasets()
cs = ChiSquared()
data.readTraining()
data.readTesting()
data.readValidation()

all_attributes = [MasterAttribute("cap-shape", 0, ["b", "c", "x", "f", "k", "s"]),
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

#dt_ent_99 = DecisionTree("Entropy Split, 99 Confidence", data.training, data.testing, all_attributes, cs, 99, True)
#dt_ent_95 = DecisionTree("Entropy Split, 95 Confidence", data.training, data.testing, all_attributes, cs, 95, True)
#dt_ent_50 = DecisionTree("Entropy Split, 50 Confidence", data.training, data.testing, all_attributes, cs, 50, True)
dt_ent_00 = DecisionTree("Entropy Split, 00 Confidence", data.training, data.testing, all_attributes, cs, 0, True)

#dt_ce_99 = DecisionTree("Class Error Split, 99 Confidence", data.training, data.testing, all_attributes, cs, 99, False)
#dt_ce_95 = DecisionTree("Class Error Split, 95 Confidence", data.training, data.testing, all_attributes, cs, 95, False)
#dt_ce_50 = DecisionTree("Class Error Split, 50 Confidence", data.training, data.testing, all_attributes, cs, 50, False)
#dt_ce_00 = DecisionTree("Class Error Split, 00 Confidence", data.training, data.testing, all_attributes, cs, 0, False)

#dt_list = [dt_ent_99, dt_ent_95, dt_ent_50, dt_ent_00, dt_ce_99, dt_ce_95, dt_ce_50, dt_ce_00]

dt_ent_00.validateSet(data.validation)
data.writeAnswerFile()
