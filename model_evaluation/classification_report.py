import numpy as np
import pprint 
from collections import defaultdict
import sys
import os

location_of_results =  os.path.join(sys.argv[1],"results.npz") 

npzfile = np.load(location_of_results) 

estimator_to_results = defaultdict(list)

for k in npzfile['arr_0']:
    
    e = k['estimator']
    
    p = tuple(sorted(tuple(k['parameters'].items()), key = lambda x: x[0]))
    
    scores = {'roc_auc_score': k['roc_auc_score'], 
              'f1_score': k['f1_score'], 
              'precision_score':k['precision_score'], 
              'recall_score':k['recall_score']}
    
    hyper_parameters_to_scores = {p:scores}
    
    estimator_to_results[e].append(hyper_parameters_to_scores)


pprint.pprint(estimator_to_results)

