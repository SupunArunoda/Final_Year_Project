from orderbook.Order import Order
from orderbook.OrderBook import OrderBook
from preprocess.static.PriceVolumeAverage import Window
from validate.preprocess.PriceVolumeAverageTest import PriceVolumeAverage
from validate.preprocess.ExecutionTypeTest import ExecutionTypeTest
#from validate.model.Kmeans import KMeans

message_file = './data/data.csv'
session_file='./data/sessions.csv'
time_framed_file='./output/time_framed_data.csv'

#Test PriceVolumeAverage
vol_average=PriceVolumeAverage()
vol_average.run_volume_average(message_file=message_file,session_file=session_file,no_of_lines=0,time_delta=300)

# ex_type_based=ExecutionTypeTest()
# ex_type_based.run_execution_type(message_file=message_file,session_file=session_file,no_of_lines=0,time_delta=300)

# count_order_type_list = [[11,7],[17,7],[36,36],[3,4]]
# col_list=[sum(x) for x in zip(*count_order_type_list)]#get column sum
# print(col_list)

#Test clustering

# kmeans=KMeans()
# kmeans.run_kmeans_cluster(file_path=time_framed_file)



