from Entity import *

'''
The Datasets class is the class responsible for reading and writing data from and
into text files. The Datasets class holds lists of objects from which we will build the
decision trees from, lists of objects which will help us judge the accuracy of our tree,
or lists of objects which need classifying
'''
class Datasets:
    def __init__(self):
        self.training = [] #list of objects to build tree from
        self.testing = [] #list of objects which will help us judge accuracy of our trees
        self.validation = [] #list of objects which need classifying

    def readTraining(self):
        with open("training.txt") as file:
            for line in file:
                self.training.append(Entity(line, True))

    def readTesting(self):
        with open("testing.txt") as file:
            for line in file:
                self.testing.append(Entity(line, True))

    def readValidation(self):
        with open("validation.txt") as file:
            for line in file:
                self.validation.append(Entity(line, True))

    def writeAnswerFile(self):
        file = open('result.txt', 'w')
        for ent in self.validation:
            file.write(ent.final_class)
            file.write('\n')
        file.close()

'''
The ChiSquared class is a simple data class which holds the necessary chi squared
statistics in a table. It also includes helper functions to read in a chi squared
table from a text file and to retrieve specific values from the chi squared table
'''
class ChiSquared:
    def __init__(self):
        self.maxDOF = 20
        self.number_alphas = 3 #only care about 3 confidence values: 99, 95, and 50. We don't do anything for 0
        self.chi_table = [[0 for x in range(self.number_alphas)] for x in range(self.maxDOF)]
        self.readChiSquaredText()

    #function which opens a file "chisquared.txt" and reads in information into
    #the chi_table data member
    def readChiSquaredText(self):
        with open("chisquared.txt") as file:
            row = 0
            for line in file:
                col = 0
                for num in line.strip().split(','):
                    self.chi_table[row][col] = float(num)
                    col += 1
                row += 1

    #function to look up an entry in the chi squared table
    #input: degrees of freedom, desired confidence level
    #output: the chi squared value at that dof and confidence value
    def lookup(self, dof, confindence):
        col = self.confidenceToCol(confindence)
        row = dof - 1
        return self.chi_table[row][col]

    #helper function to convert from requested confidence level to column in the
    #chi_table
    def confidenceToCol(self, x):
        return {
            50: 0,
            95: 1,
            99: 2,
        }[x]
