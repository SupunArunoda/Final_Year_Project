from orderbook.Order import Order
from orderbook.OrderBook import OrderBook
from preprocess.dynamic.ExecutionTypeDynamic import ExecutionTypeDynamic
from validate.preprocess.PriceVolumeAverageTest import PriceVolumeAverage
from validate.preprocess.ExecutionTypeTest import ExecutionTypeTest

import pandas as pd

from validate.model.Kmeans import KMeans

message_file = './data/data.csv'
session_file='./data/sessions.csv'
time_framed_file='./output/time_framed_data.csv'

file_a='./output/ex_type_static_normalize.csv'
file_b='./output/price_volume_average_static_normalize_7.csv'


a = pd.read_csv(file_a)
b = pd.read_csv(file_b)
b = b.dropna(axis=1)
merged = a.merge(b, on='time_index_volume')
merged.to_csv("output.csv", index=False)
ex_type_dynamic=ExecutionTypeDynamic(session_file=session_file)
n_list=ex_type_dynamic.sliding_window(iterable=range(10),size=5)
print(type(n_list))
for each in n_list:
    print(each)

# #Test PriceVolumeAverage
vol_average=PriceVolumeAverage()
vol_average.run_volume_average(message_file=message_file,session_file=session_file,no_of_lines=0,time_delta=420)

ex_type_based=ExecutionTypeTest()
ex_type_based.run_execution_type_static(message_file=message_file,session_file=session_file,no_of_lines=0,time_delta=420)

count_order_type_list = [[11,7],[17,7],[36,36],[3,4]]
col_list=[sum(x) for x in zip(*count_order_type_list)]#get column sum
print(col_list)

#Test clustering

kmeans=KMeans()
kmeans.run_kmeans_cluster(file_path=time_framed_file)

print(str("Hello"))



