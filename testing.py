from cnn_pipeline.convolutional_neural_network import design_matrix_with_target
from cnn_pipeline.classification import TrainingStack
import yaml
import sys


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


print X.shape
print y.shape

from sklearn.externals import joblib

trained_model = ts.train_classifier_interval_df(X,y)
for clf in trained_model:

def evaluate(clf,X_test,y_tue):   
    parameter_string = hashlib.md5(str(clf.get_params())).hexdigest()
    model = str(clf).split("(")[0]
    final_path = interval_name + "_"  + model +"_" + parameter_string + ".pkl"
    estimator_state_location = model_setup["model_directory"] + final_path
    joblib.dump(clf, estimator_state_location)
    result = test_classifier(clf,X_test,y_true)
    result["interval"] = interval_name
    result["model_location"] = final_path 
    if not interval_result["roc_auc_score"] - .5 <= .005:
        print interval_result 
    return interval_result





