import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import style
style.use("ggplot")

from sklearn.cluster import KMeans
from pandas import DataFrame, read_csv




class Kmeans:
    def __init__(self):
        self.model_data = DataFrame()

    def read_vector_file(self,message_file):
        read_messages = read_csv(message_file)
        #read_messages.re
       # read_messages.columns = ['Best_Bid_Ask', 'Direction', 'Execution_Time', 'Order_ID', 'Price', 'Volume','mult','time_vector','volume_vector','price_vector']
        self.model_data=read_messages
        #kmeans=KMeans(n_clusters=5)
       # kmeans.fit(self.model_data)
      #  centroids=kmeans.cluster_centers_


        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(self.model_data['time_vector'],self.model_data['volume_vector'],self.model_data['price_vector'])
        ax.set_xlabel('Time Vector')
        ax.set_ylabel('Volume Vector')
        ax.set_zlabel('Price Vector')
        plt.show()






