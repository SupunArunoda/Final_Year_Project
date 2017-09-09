from app.model.cluster.Hierarchical import Hierarchical
from app.model.cluster.KMeans import Kmeans
from pandas import read_csv


class MomentumIgnition:
    def analyze(self, file_path):
        raw_datafile = read_csv(file_path)
        # X = raw_datafile[['nom_exe_order_buy_price', 'nom_exe_order_sell_price', 'nom_exe_order_buy_volume',
        #                   'nom_exe_order_sell_volume']]
        # X = raw_datafile[['nom_exe_buy','nom_exe_sell','nom_new_buy','nom_new_sell','nom_amm_buy','nom_amm_sell',
        #                   'nom_can_buy','nom_can_sell','nom_exe_order_buy_price', 'nom_exe_order_sell_price',
        #                   'nom_exe_order_buy_volume', 'nom_exe_order_sell_volume']]
        # X = raw_datafile[['nom_amm_buy', 'nom_amm_sell']]

        # X = [[1,1],[1,2],[2,1],[1,3],[1,4],[18,19],[18,17],[20,19],[19,1],[20,1],[19,2],[1,19],[2,20],[1,21]]

        X = raw_datafile[['entropy_exec_type']]
        #
        X = X.values

        # hierarchical = Hierarchical()
        # hierarchical.cluster(data=X, distance_method="average")

        kmeans = Kmeans()
        data = kmeans.cluster(data=X)  # 0-clusters, 1-kmeans object
        kmeans.writeToCSV(clusters=data[0], kmeans=data[1], raw_datafile=raw_datafile)


