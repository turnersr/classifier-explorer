from cnn_pipeline.convolutional_neural_network import design_matrix_with_target
from cnn_pipeline.classification import TrainingStack, test_classifier
import yaml
import sys
import hashlib
from sklearn.externals import joblib
from sklearn.externals.joblib import Parallel, delayed, logger
from sklearn.base import clone

model_yaml = sys.argv[1]

stream = open(model_yaml, 'r')
model_setup = yaml.load(stream)

ts = TrainingStack()
ts.initialize_classifiers(model_setup)

positive_training_feature = model_setup["positive_train_representation"]
negative_training_feature = model_setup["negative_train_representation"]

X_train,y_train = design_matrix_with_target(positive_training_feature, negative_training_feature) 

positive_testing_feature = model_setup["positive_test_representation"]
negative_testing_feature = model_setup["negative_test_representation"]

X_test,y_test = design_matrix_with_target(positive_testing_feature, negative_testing_feature) 


def fit_eval(clf,X_train,y_train,X_test,y_test):
    clf.fit(X,y)
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
        print result 
    return result

final_results = []
total_clf = len(ts.classifiers_to_fit)
print "[x] total classifies %d" % total_clf

parallel = Parallel(n_jobs=10, verbose=1,
                        pre_dispatch='2*n_jobs')
scores = parallel(delayed(fit_eval)(clone(clf), X_train,y_train,X_test,y_test)
                  for clf in ts.classifiers_to_fit)



