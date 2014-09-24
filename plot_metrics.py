import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import cPickle as p
import pandas as pd
import sys

def plot_single_precision_recall_curve(precision_recall_curve):
    filename_to_plot = []
    for i,row in precision_recall_curve.iterrows():
        f = plt.figure()

#        estimator = row["estimator"]
        estimator = row["model_location"]
        precision = row["precision_curve"]
        recall = row["recall_curve"]
        
        title = 'Precision and Recall {0}'.format(estimator)
        filename = '_'.join(title.split())

        plt.plot(recall, precision)
        plt.xlabel('Recall')
        plt.ylabel('Precision')
        plt.ylim([0.0, 1.05])
        plt.xlim([0.0, 1.0])
        plt.title(title)
        f.savefig(filename+".png")
        filename_to_plot.append(filename)
    return filename_to_plot


def plot_single_positive_rate_curve(roc_curve):
    filename_to_plot = []
    # Needs to be refactor to handle percision and recall as a function of threshold and mothers helped
    for i,row in roc_curve.iterrows():
        f = plt.figure()

        #interval = row["interval"]
        #estimator = row["estimator"]
        estimator = row["model_location"]

        fpr = row["fpr"]
        tpr = row["tpr"]

        thresholds = row["roc_curve_thresholds"]

        title = 'ROC {0}'.format(estimator)
        filename = '_'.join(title.split())

        label_fpr = 'False Positive Rate'
        label_tpr =  'True Positive Rate'

        plt.plot(fpr, tpr)
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')


        plt.ylim([0.0, 1.05])
        plt.xlim([0.0, 1.0])
        plt.title(title)

        f.savefig(filename+".png")
        filename_to_plot.append(filename)
    return filename_to_plot



location_of_results = sys.argv[1] #"results.p"
X_train,y_train,X_test,y_test,scores = p.load(open(location_of_results))
S = pd.DataFrame(scores)

plot_single_precision_recall_curve(S)
plot_single_positive_rate_curve(S)

