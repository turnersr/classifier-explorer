from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier, GradientBoostingClassifier,AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis as QDA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.neighbors import KNeighborsClassifier
from sklearn.grid_search import ParameterGrid
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import AdaBoostClassifier
from sklearn.svm import LinearSVC
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.base import clone
from sklearn.linear_model import SGDClassifier
from sklearn.ensemble import BaggingClassifier 

from sklearn.externals import joblib
from sklearn.externals.joblib import Parallel, delayed, logger
from sklearn.base import clone

import hashlib

from sklearn.metrics import f1_score,confusion_matrix, roc_curve, roc_auc_score, auc, precision_recall_curve, precision_score,recall_score, accuracy_score, confusion_matrix

def test_classifier(clf, X_test, y_true):
    """Test a classifier and get evaluation metrics

    Parameters
    ----------
    clf : a trained classifier
    X_test : a numpy matrix of shape=(n_mothers, m_observations)
    y_true : the ground truth of the predictions shape = (n_mothers,)
    
    Returns
    ----------
    metric_row : a dictionary that stores evaluation results of the model, name of the model, parameters, and the raw predictions. 
    """
    
    metric_row = {}

    score_functions = [f1_score,precision_score,recall_score]

    y_predicted = clf.predict(X_test)

    for s_function in score_functions:
        metric_row[s_function.__name__] = s_function(y_true, y_predicted, average='weighted')
        
    # Not all classifiers can return a soft classification. 
    # So not all models will have a roc or precision and recall curves

    y_score = None

    if hasattr(clf,'predict_proba'):
        try:
            y_score = clf.predict_proba(X_test)
            metric_row["predict_probability"] = y_score
        except:
            metric_row["predict_probability"] = None
            
    if hasattr(clf,'decision_function'):
        try:
            y_score = clf.decision_function(X_test)
            metric_row["confidence_scores"] = y_score
        except:
            metric_row["confidence_scores"] = None

    if hasattr(clf, 'feature_importances_'):
        metric_row["feature_importance"] = clf.feature_importances_


    try:
        if y_score.size > 0:
            
            # sometimes y_score is a redundant matrix indicating the probability of each class.

            if len(y_score.shape) >= 2 and y_score.shape[1] >= 2:
                y_score = y_score[:,1]
            
            assert y_score.shape[0] == X_test.shape[0], "y_scores not the dimension as the test matrix"

            try:
                precision, recall, thresholds = precision_recall_curve(y_true, y_score)
                metric_row["precision_curve"] = precision
                metric_row["recall_curve"] = recall
                metric_row["precision_recall_curve_thresholds"] = thresholds
            except Exception as e:
                metric_row["precision_curve"] = None
                metric_row["recall_curve"] = None
                metric_row["precision_recall_curve_thresholds"] = None


            try:
                fpr, tpr, thresholds = roc_curve(y_true,  y_score)
                metric_row["fpr"] = fpr
                metric_row["tpr"] = tpr
                metric_row["roc_curve_thresholds"] = thresholds
                metric_row["roc_auc_score"] = auc(fpr, tpr)
            except Exception as e:
                metric_row["fpr"] = None
                metric_row["tpr"] = None
                metric_row["roc_curve_thresholds"] = None
                metric_row["roc_auc_score"] = None

    except Exception as e:
        pass
        #print(e)

    metric_row["estimator"] = str(clf).split("(")[0]
    metric_row["parameters"] = clf.get_params()
    metric_row["y_predicted"] = y_predicted

    return metric_row

def save_classifier(clf, model_directory):
    """Save a classifier

    Parameters
    ----------
    clf : classifier to be saved
    model_directory : the top-level directory of where to save the model
    
        
    Returns
    ----------
    final_path : the location of the file to load the model

    """

    parameter_string = hashlib.md5(str(clf.get_params()).encode('utf-8')).hexdigest()
    model = str(clf).split("(")[0]
    final_path = model +"_" + parameter_string + ".pkl"
    estimator_state_location = model_directory + final_path
    filenames = joblib.dump(clf, estimator_state_location)
    return final_path


def fit_save_evaluate(model_directory, clf, X_train, y_train, X_test, y_test):
    """ Fit, save, and evaluate a classifier

    Parameters
    ----------
    model_directory : the top-level directory of where to save the model
    clf : classifier 
    X_train : training data, numpy matrix of shape=(n_mothers, m_obeservations)
    y_train : ground truth labels for training data, numpy array of shape=(n_mothers,)
    X_test : testing data, numpy matrix of shape=(k_mothers, m_observations)
    y_test : ground truth labels for testing data, numpy array of shape=(n_mothers,)
    
         
    Returns
    ----------
    result : If there is an error, then None. Otherwise, return a dictionary that stores name of learning problem, model performance metircs, name of the model, parameters of model, predictions made, and the location of the trained model. 
    """

    result = None
    try:
        clf.fit(X_train,y_train)
    except Exception as e:
        return result 
    try:
        model_location = save_classifier(clf, model_directory)
        result = test_classifier(clf, X_test,y_test)
        

        result["model_location"] = model_location
        return result
    except Exception as e:
        return result 


def train_save_test_multiple_classifiers(model_directory, number_jobs, classifiers_to_fit, X_train, y_train, X_test, y_test):
    """ Fit, save, and evaluate a list of classifiers

    Parameters
    ----------
    model_directory : the top-level directory of where to save the model
    number_jobs : number of jobs to run in parallel
    classifiers_to_fit : list of instantiated sklearn classifiers
    X_train : training data, numpy matrix of shape=(n_mothers, m_obeservations)
    y_train : ground truth labels for training data, numpy array of shape=(n_mothers,)
    X_test : testing data, numpy matrix of shape=(k_mothers, m_observations)
    y_test : ground truth labels for testing data, numpy array of shape=(n_mothers,)
    
         
    Returns
    ----------
    classification_result : A list of dictionaries were each dictionary saves the name of learning problem, model performance metircs, name of the model, parameters of model, predictions made, and the location of the trained model. 
    """


    classification_result = []
    parallel = Parallel(n_jobs=number_jobs, verbose=1,
                        pre_dispatch='2*n_jobs')
    
    scores = parallel(delayed(fit_save_evaluate)(model_directory, clone(clf), 
                                                     X_train,y_train,X_test,y_test)
                   for clf in classifiers_to_fit)

#    for clf in classifiers_to_fit:
#        fit_save_evaluate(model_directory, clone(clf), X_train,y_train,X_test,y_test)
    
    # Remove all the empty results 
    for s in scores:
        if s != None:
            classification_result.append(s)
            
    return classification_result



class TrainingStack(object):
    def __init__(self):
        self.valid_classifiers = {"RandomForestClassifier": RandomForestClassifier(),
                                  "GradientBoostingClassifier":GradientBoostingClassifier(),
                                  "DecisionTreeClassifier":DecisionTreeClassifier(),
                                  "ExtraTreesClassifier":ExtraTreesClassifier(),
                                  "GaussianNB": GaussianNB(),
                                  "QDA": QDA(),
                                  "LDA": LDA(),
                                  "KNeighborsClassifier": KNeighborsClassifier(),
                                  "LogisticRegression":LogisticRegression(),
                                  "LinearSVC": LinearSVC(),
                                  "AdaBoostClassifier":AdaBoostClassifier(),
                                  "PassiveAggressiveClassifier":PassiveAggressiveClassifier(),
                                  "SGDClassifier":SGDClassifier(),
                                  "BaggingClassifier": BaggingClassifier()
                                  
                            }

        self.classifiers_to_fit = []        
    
    def initialize_classifiers(self, model_setup):

        for clf_name, clf in self.valid_classifiers.items():

            if clf_name in model_setup:
                parameter_grid = model_setup[clf_name]
                for params in ParameterGrid(parameter_grid):
                    clf.set_params(**params)
                    self.classifiers_to_fit.append(clone(clf))
            else:
                continue
        assert self.classifiers_to_fit != [], "Could not find any valid classifiers"


    def train_classifier(self,X,y):
        for clf in self.classifiers_to_fit:
            clf.fit(X,y)
            yield clf
