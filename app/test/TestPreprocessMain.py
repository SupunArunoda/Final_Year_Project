from app.orderbook.Order import Order
from app.orderbook.OrderBook import OrderBook
from app.preprocess.dynamic.ExecutionTypeDynamic import ExecutionTypeDynamic
from app.validate.preprocess.ExecutionTypeTest import ExecutionTypeTest
from app.validate.preprocess.OrderbookAttr import OrderbookAttr
from app.validate.preprocess.PriceVolumeAverageTest import PriceVolumeAverage
#from app.validate.preprocess.ExecutionTypeTest import ExecutionTypeTest
from app.validate.preprocess.ChuncksWithEventsPriceGapStaticTest import ChuncksWithEventsPriceGapStaticTest
from app.InputData import InputData

import pandas as pd

#from validate.model.Kmeans import KMeans

message_file = 'F:/Hishara/FYP/Final_Year_Project/app/data/data.csv'
session_file='F:/Hishara/FYP/Final_Year_Project/app/data/sessions.csv'
# time_framed_file='./output/time_framed_data.csv'
# regular_file = './data/price_gap_regular_norm.csv'

# file_a='./output/real/ex_type_norm_20.0.csv'
# file_b='./output/real/price_volume_avrge_norm_20.0.csv'
# #
# #
# a = pd.read_csv(file_a)
# b = pd.read_csv(file_b)
# b = b.dropna(axis=1)
# merged = a.merge(b, on='time_index_volume')
# merged.to_csv("./output/real/norm_20.0.csv", index=False)
# ex_type_dynamic=ExecutionTypeDynamic(session_file=session_file)
# n_list=ex_type_dynamic.sliding_window(iterable=range(10),size=5)
# print(type(n_list))
# for each in n_list:
#     print(each)

# #Test PriceVolumeAverage
# orderbook=OrderbookAttr()
# orderbook.run_orderbook(message_file=message_file,session_file=session_file,no_of_lines=0,time_delta=420)

ex_type_based=ExecutionTypeTest()
ex_type_based.run_execution_type_static(message_file=message_file,session_file=session_file,no_of_lines=0,time_delta=1200)
# ex_type_based.run_execution_type_static(message_file=message_file,session_file=session_file,no_of_lines=0,time_delta=360)
# ex_type_based.run_execution_type_static(message_file=message_file,session_file=session_file,no_of_lines=0,time_delta=420)
# ex_type_based.run_execution_type_static(message_file=message_file,session_file=session_file,no_of_lines=0,time_delta=600)
# ex_type_based.run_execution_type_static(message_file=message_file,session_file=session_file,no_of_lines=0,time_delta=900)
# ex_type_based.run_execution_type_static(message_file=message_file,session_file=session_file,no_of_lines=0,time_delta=1200)


# count_order_type_list = [[11,7],[17,7],[36,36],[3,4]]
# col_list=[sum(x) for x in zip(*count_order_type_list)]#get column sum
# print(col_list)

#Test clustering

# kmeans=KMeans()
# kmeans.run_kmeans_cluster(file_path=time_framed_file)

# inpudata=InputData()
# inpudata.run_data_process(message_file=message_file)

#Test PriceVolumeAverage
# price_vol_average=PriceVolumeAverage()
# price_vol_average.run_volume_average(message_file=message_file,session_file=session_file,no_of_lines=0,time_delta=1200)
# price_vol_average.run_volume_average(message_file=message_file,session_file=session_file,no_of_lines=0,time_delta=315)
# price_vol_average.run_volume_average(message_file=message_file,session_file=session_file,no_of_lines=0,time_delta=360)
# price_vol_average.run_volume_average(message_file=message_file,session_file=session_file,no_of_lines=0,time_delta=420)
# price_vol_average.run_volume_average(message_file=message_file,session_file=session_file,no_of_lines=0,time_delta=600)
# price_vol_average.run_volume_average(message_file=message_file,session_file=session_file,no_of_lines=0,time_delta=900)



#Price Gap Calculation
# pricegap_static=PriceGapStaticTest()
# pricegap_static.run_price_gap(message_file=message_file,session_file=session_file,no_of_lines=0)

# price_gap_event=ChuncksWithEventsPriceGapStaticTest()
# price_gap_event.run_price_gap(message_file=message_file,session_file=session_file,no_of_lines=0)

# oderbook=OrderbookAttr()
# oderbook.run_orderbook(message_file=message_file,session_file=session_file,no_of_lines=0)






