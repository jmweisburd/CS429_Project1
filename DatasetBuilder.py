from Entity import *

class Datasets:
    def __init__(self):
        self.training = []
        self.testing = []
        self.validation = []

    def readTraining(self):
        with open("training.txt") as file:
            for line in file:
                self.training.append(Entity(line))

    def readTesting(self):
        with open("testing.txt") as file:
            for line in file:
                self.testing.append(Entity(line))

    def readValidation(self):
        with open("validation.txt") as file:
            for line in file:
                self.validation.append(Entity(line))
