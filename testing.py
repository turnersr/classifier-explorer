from cnn_pipeline.convolutional_neural_network import *
from cnn_pipeline.classification import TrainingStack, test_classifier
import yaml
import sys
import hashlib
from sklearn.externals import joblib
from sklearn.externals.joblib import Parallel, delayed, logger
from sklearn.base import clone
from sklearn.cross_validation import train_test_split
from glob import glob

model_yaml = sys.argv[1]

stream = open(model_yaml, 'r')
model_setup = yaml.load(stream)

ts = TrainingStack()
ts.initialize_classifiers(model_setup)

positive_feature = model_setup["positive_representation"]
negative_feature = model_setup["negative_representation"]


print positive_feature
print negative_feature
X,y = design_matrix_with_target(positive_feature, negative_feature) 


print X.shape
print y.shape
# positive_feature_path_list = glob(positive_feature  + "*.features")
# print positive_feature_path_list
# RM_positive = assemble_feature_matrix(positive_feature_path_list)


def fit_eval(clf,X_train,y_train,X_test,y_test):
    clf.fit(X_train,y_train)
    r = evaluate(clf,X_test,y_test)
    return r

def evaluate(clf,X_test,y_true):  
    parameter_string = hashlib.md5(str(clf.get_params())).hexdigest()
    model = str(clf).split("(")[0]
    final_path = model +"_" + parameter_string + ".pkl"
    estimator_state_location = model_setup["model_directory"] + final_path
    joblib.dump(clf, estimator_state_location)
    result = test_classifier(clf,X_test,y_true)
    result["model_location"] = final_path 
    if not result["roc_auc_score"] - .5 <= .005:
        print result["roc_auc_score"],model
    return result

final_results = []
total_clf = len(ts.classifiers_to_fit)
print "[x] total classifies %d" % total_clf
t = X.shape[0]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=None, random_state=55)
print "[x] training set dimensions"
print X_train.shape, y_train.shape
print "[x] testing set dimensions"
print X_test.shape, y_test.shape

parallel = Parallel(n_jobs=-1, verbose=1,
                        pre_dispatch='2*n_jobs')
scores = parallel(delayed(fit_eval)(clone(clf), X_train,y_train,X_test,y_test)
                  for clf in ts.classifiers_to_fit)

import cPickle as p
all_data  = (X_train,y_train,X_test,y_test,scores)
p.dump(all_data, open("results.p", "wb"))

