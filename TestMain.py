from orderbook.Order import Order
from orderbook.OrderBook import OrderBook
from preprocess.static.PriceVolumeAverage import Window
from validate.preprocess.VolumeAverage import VolumeAverage

message_file = './data/data.csv'
session_file='./data/sessions.csv'

vol_average=VolumeAverage()
vol_average.run_volume_average(message_file=message_file,session_file=session_file,no_of_lines=500)

