import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from pyclustering.cluster.kmeans import kmeans
from pyclustering.cluster.center_initializer import kmeans_plusplus_initializer
from pyclustering.cluster import cluster_visualizer

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

visualizer = cluster_visualizer();
visualizer.append_clusters(clusters, x_train.values[:,:2]);
visualizer.show();
