from pandas import DataFrame, read_csv
from model.cluster.KMeans import Kmeans

# Retrieve Data
file_path = 'time_framed_data.csv'

X = read_csv(file_path)
X = X[['cancel_order_buy', 'cancel_order_sell', 'execute_order_buy', 'execute_order_sell', 'new_order_buy',
       'new_order_sell']]
X = X.values

Kmeans.cluster(X)