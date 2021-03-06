
#################################################
### THIS FILE WAS AUTOGENERATED! DO NOT EDIT! ###
#################################################
# file to edit: Q2.ipynb

import csv
import numpy as np  # http://www.numpy.org
import ast
from datetime import datetime
from math import log, floor, ceil
import random
import numpy as np

class Utility(object):

    # This method computes entropy for information gain
    def entropy(self, class_y):
        # Input:
        #   class_y         : list of class labels (0's and 1's)

        # TODO: Compute the entropy for a list of classes
        #
        # Example:
        #    entropy([0,0,0,1,1,1,1,1,1]) = 0.918 (rounded to three decimal places)

        entropy = 0

        for i in list(set(class_y)):
            entropy += (class_y.count(i)/len(class_y))*log((class_y.count(i)/len(class_y)),2)

        entropy = -entropy

        return entropy


    def partition_classes(self, X, y, split_attribute, split_val):
        # Inputs:
        #   X               : data containing all attributes
        #   y               : labels
        #   split_attribute : column index of the attribute to split on
        #   split_val       : a numerical value to divide the split_attribute



        # TODO: Partition the data(X) and labels(y) based on the split value - BINARY SPLIT.
        #
        # Split_val should be a numerical value
        # For example, your split_val could be the mean of the values of split_attribute
        #
        # You can perform the partition in the following way
        # Numeric Split Attribute:
        #   Split the data X into two lists(X_left and X_right) where the first list has all
        #   the rows where the split attribute is less than or equal to the split value, and the
        #   second list has all the rows where the split attribute is greater than the split
        #   value. Also create two lists(y_left and y_right) with the corresponding y labels.



        '''
        Example:



        X = [[3, 10],                 y = [1,
             [1, 22],                      1,
             [2, 28],                      0,
             [5, 32],                      0,
             [4, 32]]                      1]



        Here, columns 0 and 1 represent numeric attributes.



        Consider the case where we call the function with split_attribute = 0 and split_val = 3 (mean of column 0)
        Then we divide X into two lists - X_left, where column 0 is <= 3  and X_right, where column 0 is > 3.



        X_left = [[3, 10],                 y_left = [1,
                  [1, 22],                           1,
                  [2, 28]]                           0]



        X_right = [[5, 32],                y_right = [0,
                   [4, 32]]                           1]



        '''

        X_left = []
        X_right = []

        y_left = []
        y_right = []

        for i,j in enumerate(X):
            if j[split_attribute] <= split_val:
                X_left.append(j)
                y_left.append(y[i])

            else:
                X_right.append(j)
                y_right.append(y[i])


        return (X_left, X_right, y_left, y_right)


    def information_gain(self, previous_y, current_y):
        # Inputs:
        #   previous_y: the distribution of original labels (0's and 1's)
        #   current_y:  the distribution of labels after splitting based on a particular
        #               split attribute and split value

        # TODO: Compute and return the information gain from partitioning the previous_y labels
        # into the current_y labels.
        # You will need to use the entropy function above to compute information gain
        # Reference: http://www.cs.cmu.edu/afs/cs.cmu.edu/academic/class/15381-s06/www/DTs.pdf

        """
        Example:

        previous_y = [0,0,0,1,1,1]
        current_y = [[0,0], [1,1,1,0]]

        info_gain = 0.45915
        """

        info_gain = 0
        ### Implement your code here
        #############################################

        entropy = self.entropy(previous_y)
        left_split = current_y[0]
        right_split = current_y[1]

        # Loop through the splits and calculate the subset entropies
        to_subtract = 0
        for subset in [left_split, right_split]:
            prob = (len(subset) / len(previous_y))
            to_subtract += prob * self.entropy(subset)

        info_gain = entropy-to_subtract
        #############################################
        return info_gain


    def best_split(self, X, y):
        # Inputs:
        #   X       : Data containing all attributes
        #   y       : labels
        #   TODO    : For each node find the best split criteria and return the split attribute,
        #             spliting value along with  X_left, X_right, y_left, y_right (using partition_classes)
        #             in the dictionary format {'split_attribute':split_attribute, 'split_val':split_val,
        #             'X_left':X_left, 'X_right':X_right, 'y_left':y_left, 'y_right':y_right, 'info_gain':info_gain}
        '''

        Example:

        X = [[3, 10],                 y = [1,
             [1, 22],                      1,
             [2, 28],                      0,
             [5, 32],                      0,
             [4, 32]]                      1]

        Starting entropy: 0.971

        Calculate information gain at splits: (In this example, we are testing all values in an
        attribute as a potential split value, but you can experiment with different values in your implementation)

        feature 0:  -->    split_val = 1  -->  info_gain = 0.17
                           split_val = 2  -->  info_gain = 0.01997
                           split_val = 3  -->  info_gain = 0.01997
                           split_val = 4  -->  info_gain = 0.32
                           split_val = 5  -->  info_gain = 0

                           best info_gain = 0.32, best split_val = 4


        feature 1:  -->    split_val = 10  -->  info_gain = 0.17
                           split_val = 22  -->  info_gain = 0.41997
                           split_val = 28  -->  info_gain = 0.01997
                           split_val = 32  -->  info_gain = 0

                           best info_gain = 0.4199, best split_val = 22


       best_split_feature: 1
       best_split_val: 22

       'X_left': [[3, 10], [1, 22]]
       'X_right': [[2, 28],[5, 32], [4, 32]]

       'y_left': [1, 1]
       'y_right': [0, 0, 1]
        '''

        split_attribute = 0
        split_val = 0
        X_left, X_right, y_left, y_right = [], [], [], []

        x = []
        info_gains={}
        for i in range(len(X[0])):
            x.append((i,list(set([item[i] for item in X]))))

        for i,j in x:
            for split_value in j:
                X_left, X_right, y_left, y_right = self.partition_classes(X, y, i, split_value)
                info_gain = self.information_gain(y, [y_left, y_right])
                info_gains[(i,split_value)] = info_gain

        best_feature, best_split = max(info_gains, key=info_gains.get)

        X_left, X_right, y_left, y_right = self.partition_classes(X, y, best_feature, best_split)
        return {"X_left":X_left, "X_right":X_right, "y_left":y_left, "y_right":y_right,
                'split_attribute':best_feature, 'split_val':best_split,'info_gain':[max(info_gains.values())]}

class DecisionTree(object):
    def __init__(self, max_depth):
        # Initializing the tree as an empty dictionary or list, as preferred
        self.tree = {}
        self.max_depth = max_depth

    	
    def learn(self, X, y, par_node = {}, depth=0):
        # TODO: Train the decision tree (self.tree) using the the sample X and labels y
        # You will have to make use of the functions in Utility class to train the tree

        # par_node is a parameter that is useful to pass additional information to call
        # the learn method recursively. Its not mandatory to use this parameter

        # Use the function best_split in Utility class to get the best split and
        # data corresponding to left and right child nodes

        # One possible way of implementing the tree:
        #    Each node in self.tree could be in the form of a dictionary:
        #       https://docs.python.org/2/library/stdtypes.html#mapping-types-dict
        #    For example, a non-leaf node with two children can have a 'left' key and  a
        #    'right' key. You can add more keys which might help in classification
        #    (eg. split attr and split value)

        y_entropy = Utility().entropy(y)

        #First lets check if X or y have a length 0, if so we stop the process right here
        if len(X) == 0 or len(y) == 0:
            self.tree['element'] = 'leaf'
            self.tree['result'] = 0
            return

        #Next we check if there is only one distinct element in y, if so we stop the process right here
        if len(set(y)) == 1:
            # if all same in y
            self.tree['element'] = 'leaf'
            self.tree['result'] = y[0]
            return

        #Next we begin the recursive learning process
        #Here we are counting the number of occurences of each value in y and putting results in a dictionary
        y_dict = {}
        for y_i in y:
            if y_i in y_dict.keys():
                y_dict[y_i] += 1
            else:
                y_dict[y_i] = 1

        #Now we get the max value and its corresponding key
        max_y_val = [key for key, value in y_dict.items() if value == max(y_dict.values())]
        max_y_count = max(y_dict, key=y_dict.get)

        #Now we check whether all the values of X are the same
        if all(x == X[0] for x in X):
            all_same_check = True
        else:
            all_same_check = False


        if all_same_check or depth == self.max_depth:
            self.tree['element'] = 'leaf'
            self.tree['result'] = max_y_val
            return

        #Now that the checks are done, we can begin the recursive splitting
        #We use the best_split function from the Utility class to perform the split
        split_results = Utility().best_split(X, y)

        split_column = split_results['split_attribute']
        split_value = split_results['split_val']
        X_left = split_results["X_left"]
        X_right = split_results["X_right"]
        y_left = split_results["y_left"]
        y_right = split_results["y_right"]


        self.tree['element'] = "parent"
        self.tree['result'] = "Null"

        self.tree['split_attr'] = split_column
        self.tree['split_val'] = split_value

        #Here we begin the recursion
        self.tree['left'] = DecisionTree(self.max_depth)
        self.tree['left'].learn(X_left, y_left, self, depth+1)

        self.tree['right'] = DecisionTree(self.max_depth)
        self.tree['right'].learn(X_right, y_right, self, depth+1)


    def classify(self, record):
        # TODO: classify the record using self.tree and return the predicted label
        if self.tree['element']=='leaf':
            return self.tree['result']

        else:
            attr = record[self.tree['split_attr']]
            value = self.tree['split_val']

            if isinstance(attr, str):
                if attr == value:
                    return self.tree['left'].classify(record)
                else:
                    return self.tree['right'].classify(record)
            else:
                if attr <= value:
                    return self.tree['left'].classify(record)
                else:
                    return self.tree['right'].classify(record)




# This starter code does not run. You will have to add your changes and
# turn in code that runs properly.

"""
Here,
1. X is assumed to be a matrix with n rows and d columns where n is the
number of total records and d is the number of features of each record.
2. y is assumed to be a vector of labels of length n.
3. XX is similar to X, except that XX also contains the data label for each
record.
"""

"""
This skeleton is provided to help you implement the assignment.You must
implement the existing functions as necessary. You may add new functions
as long as they are called from within the given classes.

VERY IMPORTANT!
Do NOT change the signature of the given functions.
Do NOT change any part of the main function APART from the forest_size parameter.
"""


class RandomForest(object):
    num_trees = 0
    decision_trees = []

    # the bootstrapping datasets for trees
    # bootstraps_datasets is a list of lists, where each list in bootstraps_datasets is a bootstrapped dataset.
    bootstraps_datasets = []

    # the true class labels, corresponding to records in the bootstrapping datasets
    # bootstraps_labels is a list of lists, where the 'i'th list contains the labels corresponding to records in
    # the 'i'th bootstrapped dataset.
    bootstraps_labels = []

    def __init__(self, num_trees):
        # Initialization done here
        self.num_trees = num_trees
        self.decision_trees = [DecisionTree(max_depth=5) for i in range(num_trees)]
        self.bootstraps_datasets = []
        self.bootstraps_labels = []

    def _bootstrapping(self, XX, n):
        # Reference: https://en.wikipedia.org/wiki/Bootstrapping_(statistics)
        #
        # TODO: Create a sample dataset of size n by sampling with replacement
        #       from the original dataset XX.
        # Note that you would also need to record the corresponding class labels
        # for the sampled records for training purposes.

        sample = [] # sampled dataset
        labels = []  # class labels for the sampled records

        #Here we are using bootstrapping to create the dataset that will be used in the many decision trees

        random_choice = np.random.choice(len(XX), n)
        raw_samples = [XX[i] for i in random_choice]

        labels = [row[-1] for row in raw_samples]
        samples = [row[:-1] for row in raw_samples]

        return (sample, labels)

    def bootstrapping(self, XX):
        # Initializing the bootstap datasets for each tree
        for i in range(self.num_trees):
            data_sample, data_label = self._bootstrapping(XX, len(XX))
            self.bootstraps_datasets.append(data_sample)
            self.bootstraps_labels.append(data_label)



    def fitting(self):
        # TODO: Train `num_trees` decision trees using the bootstraps datasets
        # and labels by calling the learn function from your DecisionTree class.

        #Here we create the decision trees that will later be used to vote on the result.
        for i in range(self.num_trees):
            self.decision_trees[i].learn(self.bootstraps_datasets[i], self.bootstraps_labels[i])




    def voting(self, X):
        y = []

        for record in X:
            # Following steps have been performed here:
            #   1. Find the set of trees that consider the record as an
            #      out-of-bag sample.
            #   2. Predict the label using each of the above found trees.
            #   3. Use majority vote to find the final label for this recod.
            votes = []

            for i in range(len(self.bootstraps_datasets)):
                dataset = self.bootstraps_datasets[i]

                if record not in dataset:
                    OOB_tree = self.decision_trees[i]
                    effective_vote = OOB_tree.classify(record)
                    votes.append(effective_vote)

            counts = np.bincount(votes)

            if len(counts) == 0:
                # TODO: Special case
                #  Handle the case where the record is not an out-of-bag sample
                #  for any of the trees.
                # NOTE - you can add few lines of codes above (but inside voting) to make this work

                #First we use the decision trees to classify the record
                for tree in self.decision_trees:
                    votes.append(tree.classify(record))

                #next we tally up the classifications and find the winner of the vote
                counts = np.bincount(votes)
                y = np.append(y, np.argmax(counts))

            else:
                y = np.append(y, np.argmax(counts))

        return y

    def user(self):
        """
        :return: string
        your GTUsername, NOT your 9-Digit GTId
        """
        ### Implement your code here
        #############################################
        return 'zstinnett3'
        #############################################


# TODO: Determine the forest size according to your implementation.
# This function will be used by the autograder to set your forest size during testing
# VERY IMPORTANT: Minimum forest_size should be 10
def get_forest_size():
    forest_size = 10
    return forest_size

# TODO: Determine random seed to set for reproducibility
# This function will be used by the autograder to set the random seed to obtain the same results you achieve locally
def get_random_seed():
    random_seed = 0
    return random_seed