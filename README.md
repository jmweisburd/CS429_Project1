# CS429_Project1

CS429/529 Project 1
Detection of poisonous mushrooms with Decision Trees
Julian Weisburd
Ashutosh Tripathi

This program is written in python. To use the program please enter into your terminal:
python main.py


This program produces decision trees to help classify a mushroom as either "poisonous" or "edible."
Decision trees are made using the ID3 and a training set of data which is provided with the code. 
This file is called "training.txt"
The decision trees are pruned using a chi-square metric.
The decision trees are judged on accuracy using a testing set of data which is provided with the code.
This file is called "testing.txt"
Finally, the best decision tree is selected and, using this tree, a set of mushrooms whose classifications
are unknown are evaluated. This set of validation mushrooms is provided with the code.
This file is called "validation.txt"
The classifications of the validation set of mushrooms are saved in a file "results.txt" which hopefully
will be overwritten everytime the code is ran.

A more comprehensive overview of how the code works is included in the project report.

For an overview of who contributed to the project, please check out our github repo at:
https://github.com/jmweisburd/CS429_Project1/graphs/contributors

I urge you to check out the link. I think it's pretty interesting.

Thank you
