from classification import TrainingStack, train_save_test_multiple_classifiers
import yaml
import sys
from sklearn.cross_validation import train_test_split
import numpy as np

model_yaml = sys.argv[1]

stream = open(model_yaml, 'r')
model_setup = yaml.load(stream)

classifier_stack = TrainingStack()
classifier_stack.initialize_classifiers(model_setup)

X = np.load(model_setup["X"])
y = np.load(model_setup["y"])

#print positive_feature
#print negative_feature
#X,y = design_matrix_with_target(positive_feature, negative_feature) 

print(X.shape)
print(y.shape)

final_results = []
total_clf = len(classifier_stack.classifiers_to_fit)
print("[x] total classifies %d" % total_clf)
t = X.shape[0]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=None, random_state=55)

print("[x] training set dimensions")
print(X_train.shape, y_train.shape)
print("[x] testing set dimensions")
print(X_test.shape, y_test.shape)

location_to_save_models = model_setup["model_directory"]
location_to_save_model_metrics = model_setup["metric_directory"]
number_jobs = -1

classifiers_to_fit = classifier_stack.classifiers_to_fit
scores = train_save_test_multiple_classifiers(location_to_save_models, number_jobs, classifiers_to_fit, X_train, y_train, X_test, y_test)
#print(scores)
np.savez(location_to_save_model_metrics+"/results", scores,X_train,y_train,X_test,y_test)
