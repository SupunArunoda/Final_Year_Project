from model.cluster.Hierarchical import Hierarchical
from model.cluster.KMeans import Kmeans
from pandas import read_csv


class MomentumIgnition:
    def analyze(self, file_path):
        raw_datafile = read_csv(file_path)
        # X = raw_datafile[['nom_exe_order_buy_price', 'nom_exe_order_sell_price', 'nom_exe_order_buy_volume',
        #                   'nom_exe_order_sell_volume']]
        # X = raw_datafile[['nom_exe_buy','nom_exe_sell','nom_new_buy','nom_new_sell','nom_amm_buy','nom_amm_sell',
        #                   'nom_can_buy','nom_can_sell','nom_exe_order_buy_price', 'nom_exe_order_sell_price', 'nom_exe_order_buy_volume',
        #                   'nom_exe_order_sell_volume']]
        X = raw_datafile[['nom_exe_buy', 'nom_exe_sell', 'nom_new_buy', 'nom_new_sell',
                          'nom_can_buy', 'nom_can_sell']]

        X = X.values

        hierarchical = Hierarchical()
        hierarchical.cluster(data=X)

        # kmeans = Kmeans
        # kmeans.cluster(data=X)
