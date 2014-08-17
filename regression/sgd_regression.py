
# coding: utf-8

# In[99]:

import sklearn
import numpy as np


# In[10]:

e = numpy.random.random((300000, 4096))


# In[86]:

e.shape


# In[11]:

y_test = numpy.random.random((300000, ))


# In[12]:

y_train = numpy.random.random((300000, ))


# In[29]:

from sklearn.linear_model import SGDRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.grid_search import ParameterGrid
from sklearn.base import clone


# In[124]:

sgd_grid= {"learning_rate":['invscaling'], "eta0": [0.01, .001, .0001], "l1_ratio": [0.15, 0.3, 0.4, .5, .01, .05], "alpha":[0.0001, .1, 0.001, 0.01] }


# In[125]:

def initialize_regressors(sgd_grid):
    l = SGDRegressor()
    regressions_to_fit = []
    for params in ParameterGrid(sgd_grid):
        l.set_params(**params)
        regressions_to_fit.append(clone(l))
    return regressions_to_fit


# In[126]:

regressions_to_fit = initialize_regressors(sgd_grid)
print len(regressions_to_fit)


# In[127]:

def train_regression(regessions,X,y):
    for reg in regessions:
        print str(reg)
        reg.fit(X,y)
        yield reg


# In[128]:

fitted_regression = train_regression(regressions_to_fit,e,y_train)


# In[129]:

from sklearn.metrics import explained_variance_score, mean_absolute_error, mean_squared_error, r2_score


# In[ ]:

count = 0
global_model_results = []
start_time = time.time()
for fitted in fitted_regression:
    local_model_results = {}
    y_predicted = fitted.predict(e)
    mse = mean_squared_error(y_test, y_predicted)
    evs = explained_variance_score(y_test, y_predicted)
    mae = mean_absolute_error(y_test, y_predicted)
    r2 = r2_score(y_test, y_predicted)
    parameters = fitted.get_params()
    local_model_results["parameters"] = parameters
    local_model_results["mean_squared_error"] = mse
    local_model_results["explained_variance_score"] = evs
    local_model_results["mean_absolute_error"] = mae
    local_model_results["r2_score"] = r2
    
    global_model_results.append(local_model_results)
    count += 1
    print count
end_time = time.time() - start_time


# In[82]:

len(regressions_to_fit)


# In[63]:

global_model_results


# In[66]:

time.time()


# In[ ]:

import multiprocessing, numpy, ctypes


# In[ ]:



