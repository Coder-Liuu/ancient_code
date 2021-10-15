from sklearn.mixture import GaussianMixture
from pyclustering.cluster.clique import clique
from sklearn.cluster import MeanShift, estimate_bandwidth 
import numpy as np

class GMM:
    def __init__(self,n_clusters,max_iter):
        self.GMM = GaussianMixture(n_components=n_clusters,max_iter=max_iter)
        self.labels_ = None
    def fit(self,data):
        self.GMM.fit(data)
        self.labels_ = self.GMM.predict(data)

class CLIQUE:
    def __init__(self,intervals,threshold):
        self.intervals = intervals
        self.threshold = threshold

    def fit(self,data):
        data = data.values
        self.CLIQUE = clique(data,self.intervals,self.threshold)
        self.CLIQUE.process()
        preds = self.CLIQUE.get_clusters()
        
        self.labels_ = np.empty(data.shape[0],dtype=int)
        for id_,pred in enumerate(preds):
            for i in pred:
                self.labels_[i] = id_

class MEANSHIFT:
    def __init__(self,quantile,n_samples):
        self.quantile = quantile
        self.n_samples = n_samples

    def fit(self,data):
        bandwidth = estimate_bandwidth(data, quantile=self.quantile, n_samples=self.n_samples)
        self.MeanShift = MeanShift(bandwidth=bandwidth)
        self.MeanShift.fit(data)
        self.labels_ = self.MeanShift.labels_

if __name__ == "__main__":
    import pandas as pd
    import matplotlib.pyplot as plt
    data = pd.read_csv("data/iris.csv").values
    clf = MEANSHIFT(0.2,500)
    clf.fit(data)
