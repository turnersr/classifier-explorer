import numpy as np
from glob import glob
#from ..data_ingestion_and_creation.test import goo

def overfeat_to_numpy(feature_path):
    final = []
    fr = open(feature_path)
    for line in fr.readlines():
        linearr = line.strip().split()
        linearr = map(float,linearr)
        final.append(linearr)
    e = np.matrix(final[1:])
    return e


def assemble_feature_matrix(feature_path_list):
    features = []
    for f in feature_path_list:
        features.append(overfeat_to_numpy(f))
    RM = np.vstack(features)
    return RM

def design_matrix_with_target(positive_examples,negative_examples):

    positive_feature_path_list = glob(positive_examples + "*.features")
    RM_positive = assemble_feature_matrix(positive_feature_path_list)

    negative_feature_path_list = glob(negative_examples + "*.features")
    RM_negative = assemble_feature_matrix(negative_feature_path_list )

    y_neg = np.zeros(RM_negative.shape[0])
    y_pos = np.ones(RM_positive.shape[0])
    
    print RM_positive.shape
    print RM_negative.shape

    print y_neg.shape
    print y_pos.shape
    X = np.vstack((RM_positive, RM_negative))
    y = np.hstack((y_pos,y_neg))

    #X = X.view('float32')
    return X,y
