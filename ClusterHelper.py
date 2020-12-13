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
from sklearn.cluster import KMeans,Birch,DBSCAN,OPTICS,MeanShift
from sklearn.mixture import GaussianMixture
from pyclustering.cluster.clique import clique
from sklearn.manifold import TSNE


class ClusterHelper:
    def __init__(self):
        self.cluster = None

    def set_Cluster(self,algorithm):
        if algorithm == "KMeans":
            self.cluster = KMeans(3)
        elif algorithm == "BIRCH":
            self.cluster = Birch(3)
        elif algorithm == "DBSCAN":
            self.cluster = DBSCAN(eps=2,min_samples=2)
        elif algorithm == "GMM":
            self.cluster = GaussianMixture(n_components=3,max_iter= 100)
        elif algorithm == "OPTICS":
            self.cluster = OPTICS()
        elif algorithm == "MeanShift":
            self.cluster = MeanShift()
        elif algorithm == "CLIQUE":
            self.cluster = clique()
        else:
            print("没有找到分类器")

    def fit(self,data):
        if(self.cluster == None):
            print("请初始化聚类器")
            exit(0)
        self.data = data.copy()
        self.labels = self.data.pop("class").values

        if isinstance(self.cluster,clique):
            self.cluster.process()
            # TODO: 完成clique的训练过程
        else:
            self.cluster.fit(data)

    def get_score(self,name="None"):
        if isinstance(self.cluster,GaussianMixture):
            self.pred = self.cluster.predict(data)
        else:
            self.pred = self.cluster.labels_

        self.class_ = np.unique(self.pred)
        score = {}
        score1 = silhouette_score(self.pred.reshape(-1,1),self.labels)
        score2 = metrics.adjusted_rand_score(self.pred,self.labels)

        score["轮廓系数"] = score1
        score["调整兰德系数"] = score2
        return score

    def imshow(self):
        for i in self.class_:
            d=self.data[self.pred==i].values
            plt.scatter(d[:,0],d[:,1])
        plt.show()

if __name__ == "__main__":
    data = pd.read_csv("data/iris.csv")

    cluster = ClusterHelper()
    cluster.set_Cluster("MeanShift")
    cluster.fit(data)
    score = cluster.get_score("轮廓系数")
    cluster.imshow()
    print(score)
