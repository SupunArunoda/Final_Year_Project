from pandas import DataFrame, read_csv
from app.model.cluster.KMeans import Kmeans

class KMeans:

    def run_kmeans_cluster(self,file_path):
        X = read_csv(file_path)
        # X = X.values

        Kmeans.cluster(X)
