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
from sklearn.cluster import KMeans,Birch,DBSCAN,OPTICS
from pyclustering.cluster.clique import clique
from sklearn.manifold import TSNE
from packing import GMM,CLIQUE,MEANSHIFT


class ClusterHelper:
    def __init__(self):
        self.cluster = None

    def set_Cluster(self,algorithm,param_dict):
        self.algorithm_name = algorithm
        if algorithm == "KMeans":
            self.cluster = KMeans(param_dict[0],max_iter=param_dict[1])
        elif algorithm == "BIRCH":
            self.cluster = Birch(n_clusters=param_dict[0],threshold=param_dict[1])
        elif algorithm == "DBSCAN":
            self.cluster = DBSCAN(eps=param_dict[0],min_samples=param_dict[1])
        elif algorithm == "GMM":
            self.cluster = GMM(n_clusters=param_dict[0],max_iter=param_dict[1])
        elif algorithm == "OPTICS":
            self.cluster = OPTICS(min_samples=param_dict[0],max_eps=param_dict[1])
        elif algorithm == "MeanShift":
            self.cluster = MEANSHIFT(quantile=param_dict[0],n_samples=param_dict[1])
        elif algorithm == "CLIQUE":
            self.cluster = CLIQUE(intervals=param_dict[0],threshold=param_dict[1])
        else:
            print("没有找到分类器")
        self.cluster.class_ = None

    def fit(self,data):
        if(self.cluster == None):
            print("请初始化聚类器")
            exit(0)
        self.data = data.copy()
        self.labels = self.data.pop("class").values

        self.cluster.fit(data)

    def get_score(self,name="None"):
        self.pred = self.cluster.labels_
        self.pred = np.where(self.pred > 1000,-1,self.pred)

        self.class_ = np.unique(self.pred)
        score = {}
        score1 = silhouette_score(self.pred.reshape(-1,1),self.labels)
        score2 = metrics.adjusted_rand_score(self.pred,self.labels)

        score["轮廓系数"] = score1
        score["调整兰德系数"] = score2
        return score

    def imshow(self):
        yshape = self.data.shape[1]
        fig = plt.figure()
        fig.canvas.set_window_title(self.algorithm_name)
        for i in range(yshape):
            for j in range(yshape):
                plt.subplot(yshape,yshape,i*yshape+j+1)
                for class_ in self.class_:
                    d=self.data[self.pred==class_].values
                    plt.scatter(d[:,i],d[:,j],label=class_)
        plt.legend()
        plt.show()

if __name__ == "__main__":
    data = pd.read_csv("data/ecoli1.csv")
    cluster = ClusterHelper()
    cluster.set_Cluster("KMeans",[3,100])
    cluster.fit(data)
    score = cluster.get_score("轮廓系数")
    cluster.imshow()
    print(score)
