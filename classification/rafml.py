from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier, GradientBoostingClassifier,AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.qda import QDA
from sklearn.lda import LDA
from sklearn.neighbors import KNeighborsClassifier
from sklearn.grid_search import ParameterGrid
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import AdaBoostClassifier
from sklearn.svm import LinearSVC
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.base import clone
from sklearn.linear_model import SGDClassifier
from sklearn.ensemble import BaggingClassifier 

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
        metric_row[s_function.__name__] = s_function(y_true,y_predicted)
        
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
        if y_score != None:
            
            # sometimes y_score is a redundant matrix indicating the probability of each class. 
            if len(y_score.shape) >= 2 and y_score.shape[1] >= 2:
                y_score = y_score[:,1]
            
            assert y_score.shape[0] == X_test.shape[0], "y_scores not the dimension as the test matrix" 
            precision, recall, thresholds = precision_recall_curve(y_true, y_score)
            metric_row["precision_curve"] = precision
            metric_row["recall_curve"] = recall
            metric_row["precision_recall_curve_thresholds"] = thresholds
            fpr, tpr, thresholds = roc_curve(y_true,  y_score)
            metric_row["fpr"] = fpr
            metric_row["tpr"] = tpr
            metric_row["roc_curve_thresholds"] = thresholds
            metric_row["roc_auc_score"] = auc(fpr, tpr)

            

    except Exception, e:
        #print e
        metric_row["precision_curve"] = None
        metric_row["recall_curve"] = None
        metric_row["precision_recall_curve_thresholds"] = None
        metric_row["fpr"] = None
        metric_row["tpr"] = None
        metric_row["roc_curve_thresholds"] = None
        metric_row["roc_auc_score"] = None

    metric_row["estimator"] = str(clf).split("(")[0]
    metric_row["parameters"] = clf.get_params()
    metric_row["y_predicted"] = y_predicted
    return metric_row

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
