from sklearn.mixture import GaussianMixture
from pyclustering.cluster.clique import clique
import numpy as np

class GMM:
    def __init__(self):
        self.GMM = GaussianMixture(3)
        self.labels_ = None
    def fit(self,data):
        self.GMM.fit(data)
        self.labels_ = self.GMM.predict(data)

class CLIQUE:
    def __init__(self):
        pass

    def fit(self,data):
        data = data.values
        self.CLIQUE = clique(data,5,0)
        self.CLIQUE.process()
        preds = self.CLIQUE.get_clusters()
        
        self.labels_ = np.empty(data.shape[0],dtype=int)
        for id_,pred in enumerate(preds):
            for i in pred:
                self.labels_[i] = id_

if __name__ == "__main__":
    import pandas as pd
    import matplotlib.pyplot as plt
    data = pd.read_csv("data/iris.csv").values
    clf = CLIQUE()
    clf.fit(data)
