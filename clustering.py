import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from pyclustering.cluster.kmeans import kmeans
from pyclustering.cluster.center_initializer import kmeans_plusplus_initializer
from pyclustering.cluster import cluster_visualizer
from pyclustering.cluster.silhouette import silhouette
from sklearn.metrics.cluster import silhouette_score


# ----------------
n_clusters = 4
# ----------------

data = pd.read_csv("data/iris.csv")
labels = data.pop("class")

x_train,y_train,x_test,y_test = train_test_split(data,labels,test_size=3)

initial_centers = kmeans_plusplus_initializer(x_train, 3).initialize()
kmeans_instance = kmeans(x_train,initial_centers);

kmeans_instance.process();
clusters = kmeans_instance.get_clusters();
a = np.zeros(x_train.shape[0],dtype=int)

for i in range(1,len(a)+1):
    for id_,cluster in enumerate(clusters):
        if( i in cluster):
            a[i-1] = id_
            break;

# a = a.reshape(-1,1)
# print(x_test.values)
# exit(0)
# 计算轮廓系数
score2 = silhouette_score(a,x_test.values,metric='euclidean')
print(score2)

score = silhouette(x_train.values, clusters).process().get_score()
print(sum(score)/len(score))

# 可视化
# visualizer = cluster_visualizer();
# visualizer.append_clusters(clusters, x_train.values[:,:2]);
# visualizer.show();
