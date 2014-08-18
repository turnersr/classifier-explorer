import cPickle as p
import pandas as pd
location_of_results = "results.p"
X_train,y_train,X_test,y_test,scores = p.load(open(location_of_results))
S = pd.DataFrame(scores)
