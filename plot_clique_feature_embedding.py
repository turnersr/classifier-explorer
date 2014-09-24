import pandas as pd
from collections import defaultdict
import cPickle as p
import networkx as nx
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import sys
from itertools import combinations_with_replacement

from sklearn import (manifold, datasets, decomposition, ensemble, lda,
                     random_projection)


def top_n_feature_network(feature_importance_matrix, top_n):
    SD = np.argsort(-feature_importance_matrix)

    G=nx.Graph()
    for x in SD[:,0:top_n]:
        for edge in combinations_with_replacement(x, 2):
            if edge in G.edges():            
                weight = G.get_edge_data(*edge)["count"]
                weight_ = weight + 1

                G.add_edge(*edge,count=weight_)
            else:
                G.add_edge(*edge,count=1)   
    return G


def plot_embedding(feature_reduction_df, color, title):
    filename = "_".join(title.split(" "))
    fig = plt.figure()
    plt.scatter(feature_reduction_df["X"], feature_reduction_df["Y"], c=color)
    plt.title(title)
    cb = plt.colorbar()
    #  cb.set_label('Probability of ') 
    fig.savefig(filename+".png",bbox_inches='tight')



location_of_results = sys.argv[1]

X_train,y_train,X_test,y_test,scores = p.load(open(location_of_results))
run_results = pd.DataFrame(scores)

feature_importance = run_results[pd.notnull(run_results["feature_importance"])]
feature_importance = feature_importance["feature_importance"]

M1 = feature_importance.as_matrix().tolist()
feature_importance_matrix = np.array(M1)


networkx_graph = top_n_feature_network(feature_importance_matrix, 5)

clique_features = list(nx.find_cliques(networkx_graph))

print clique_features

print len(clique_features)





# n_neighbors = 10
# n_components = 2


# # In[ ]:

# isomap = manifold.Isomap(n_neighbors, n_components)
# LLE = manifold.LocallyLinearEmbedding(n_neighbors, n_components)

# print "Isomapping"
# for interval in R:
#     inteval_name = interval[0]
#     print inteval_name
#     for clique_crosstab in interval[1]:
        
#         UNRolled = decompose_crosstab(clique_crosstab)
#         feature_name = clique_crosstab.index.names[0]
#         color = UNRolled["dropout_probability"]
        
#         X = UNRolled.drop(["remain_probability",'dropout_probability'], axis=1)
#         X_isomap = LLE.fit_transform(X)
        
#         feature_reduction_df = pd.DataFrame(X_isomap, columns=["X","Y"])

#         title = inteval_name + " " + "LLE" + " " + feature_name
#         print title

#         plot_embedding(feature_reduction_df, color, title)
