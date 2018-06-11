from sklearn.datasets import make_classification
import numpy as np

X, y = make_classification(n_samples=500,
                           n_features=20,
                           n_informative=5,
                           n_redundant=0,
                           n_repeated=0,
                           n_classes=2,
                           random_state=0,
                           shuffle=False)


np.save("../datasets/X", X)
np.save("../datasets/y", y)





