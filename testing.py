from cnn_pipeline.convolutional_neural_network import *
from cnn_pipeline.classification import TrainingStack, train_save_test_multiple_classifiers
import yaml
import sys

from sklearn.cross_validation import train_test_split

model_yaml = sys.argv[1]

stream = open(model_yaml, 'r')
model_setup = yaml.load(stream)

classifier_stack = TrainingStack()
classifier_stack.initialize_classifiers(model_setup)

positive_feature = model_setup["positive_representation"]
negative_feature = model_setup["negative_representation"]

print positive_feature
print negative_feature
X,y = design_matrix_with_target(positive_feature, negative_feature) 

print X.shape
print y.shape

final_results = []
total_clf = len(classifier_stack.classifiers_to_fit)
print "[x] total classifies %d" % total_clf
t = X.shape[0]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=None, random_state=55)
print "[x] training set dimensions"
print X_train.shape, y_train.shape
print "[x] testing set dimensions"
print X_test.shape, y_test.shape

location_to_save_models = model_setup["model_directory"]
number_jobs = -1
classifiers_to_fit = classifier_stack.classifiers_to_fit

scores = train_save_test_multiple_classifiers(location_to_save_models, number_jobs, classifiers_to_fit, X_train, y_train, X_test, y_test)

import cPickle as p
all_data  = (X_train,y_train,X_test,y_test,scores)
p.dump(all_data, open("results.p", "wb"))
