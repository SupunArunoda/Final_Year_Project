from app.model.cluster.KMeans import Kmeans
from pandas import read_csv


class MomentumIgnition:
    def analyze(self, file_path):
        raw_datafile = read_csv(file_path)

        X = raw_datafile[['nom_exe_order_buy_price',
                          'nom_exe_order_sell_price', 'nom_exe_order_buy_volume', 'nom_exe_order_sell_volume']]


        X = X.values

        # hierarchical = Hierarchical()
        # hierarchical.cluster(data=X, distance_method="average")

        kmeans = Kmeans()
        data = kmeans.cluster(data=X)  # 0-clusters, 1-kmeans object
        kmeans.writeToCSV(clusters=data[0], kmeans=data[1], raw_datafile=raw_datafile)


