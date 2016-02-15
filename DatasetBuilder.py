from Entity import *


class Datasets:
    def __init__(self):
        self.training = []
        self.testing = []
        self.validation = []

    def readTraining(self):
        with open("training.txt") as file:
            for line in file:
                self.training.append(Entity(line, True))

    def readTesting(self):
        with open("testing.txt") as file:
            for line in file:
                self.testing.append(Entity(line))

    def readValidation(self):
        with open("validation.txt") as file:
            for line in file:
                self.validation.append(Entity(line))


class ChiSquared:

    def __init__(self):
        self.maxDOF = 20
        self.number_alphas = 3
        self.chi_table = [[0 for x in range(self.number_alphas)] for x in range(self.maxDOF)]
        self.readChiSquaredText()

    def readChiSquaredText(self):
        with open("chisquared.txt") as file:
            row = 0
            for line in file:
                col = 0
                for num in line.strip().split(','):
                    self.chi_table[row][col] = float(num)
                    col += 1
                row += 1

    def printChiSquaredTable(self):
        for row in range(0,19):
            for col in range(0,3):
                print self.chi_table[row][col]


    def lookup(self, dof, confindence):
        col = self.confidenceToCol(confindence)
        row = dof - 1
        return self.chi_table[row][col]

    def confidenceToCol(self, x):
        return {
            50: 0,
            95: 1,
            99: 2,
        }[x]
