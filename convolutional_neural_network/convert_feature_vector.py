import numpy as np
import glob as g

feature_dir = "/mnt/data/nfp_bk/nfp3/OverFeat/representation/"

def overfeat_to_numpy(feature_path):
    final = []
    fr = open(feature_path)
    for line in fr.readlines():
        linearr = line.strip().split()
        final.append(linearr)
    e = np.matrix(final[1:])
    return e


def assemble_feature_matrix(feature_path_list):
    features = []
    for f in feature_path_list:
        features.append(overfeat_to_numpy(f))
    RM = np.vstack(features)
    return RM


feature_path_list = g.glob(feature_dir + "*.features")
RM = assemble_feature_matrix(feature_path_list )
