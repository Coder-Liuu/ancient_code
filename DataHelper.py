import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class DataHelper:
    def __init__(self,path):
        self.read_data(path)

    def read_data(self,path):
        self.data = pd.read_csv(path)
        self.class_ = len(self.data["class"].unique())
        self.shape = self.data.shape

if __name__ == "__main__":
    
    dataHelper = DataHelper("data/iris.csv")
    print(str(dataHelper.class_))
    print(str(dataHelper.shape))
