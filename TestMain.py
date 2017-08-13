from orderbook.Order import Order
from orderbook.OrderBook import OrderBook
from preprocess.static.PriceVolumeAverage import Window
from validate.preprocess.PriceVolumeAverage import PriceVolumeAverage
from validate.model.Kmeans import KMeans

message_file = './data/data.csv'
session_file='./data/sessions.csv'
time_framed_file='./output/time_framed_data.csv'

#Test PriceVolumeAverage
# vol_average=PriceVolumeAverage()
# vol_average.run_volume_average(message_file=message_file,session_file=session_file,no_of_lines=500)

#Test clustering

kmeans=KMeans()
kmeans.run_kmeans_cluster(file_path=time_framed_file)



