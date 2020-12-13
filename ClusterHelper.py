import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from pyclustering.cluster.kmeans import kmeans
from pyclustering.cluster.center_initializer import kmeans_plusplus_initializer
from pyclustering.cluster import cluster_visualizer
from pyclustering.cluster.silhouette import silhouette
from sklearn import metrics
from sklearn.metrics.cluster import silhouette_score
from sklearn.cluster import KMeans


class ClusterHelper:
    def __init__(self):
        self.cluster = None

    def set_Cluster(self):
        self.cluster = KMeans(3)

    def fit(self,data):
        if(self.cluster == None):
            print("请初始化聚类器")
            return
        self.labels = data.pop("class")
        self.cluster.fit()

    def get_score(self,name="None"):
        pred = self.cluster.labels_
        if(name == "轮廓系数"):
            score = silhouette_score(pred.reshape(-1,1),labels.values)
        elif(name == "调整兰德系数"):
            score = metrics.adjusted_rand_score(pred,labels.values)

# # ----------------
# n_clusters = 3
# # ----------------

# data = pd.read_csv("data/iris.csv")
# labels = data.pop("class")

# cls = KMeans(3)
# # print(isinstance(data,KMeans))
# exit(0)
# cls.fit(data)
# a = cls.labels_

# score = silhouette_score(a.reshape(-1,1),labels.values)
# print("轮廓系数:",score)
# score2 = metrics.adjusted_rand_score(a,labels.values)
# print("调整兰德系数:",score2)