from app.orderbook.Order import Order
from app.orderbook.OrderBook import OrderBook
from pandas import read_csv
from app.preprocess.static.PriceVolumeAverage import Window
from pandas import DataFrame, read_csv
from app.preprocess.static.ExecutionTypeStatic import ExecutionTypeStatic
import numpy as np


class Main:
    def __init__(self):
        self.normalize_data_frame = DataFrame()

    def run_volume_average(self, message_file, session_file, no_of_lines, time_delta):

        read_messages = read_csv(message_file, header=None)
        read_messages.columns = ['instrument_id', 'broker_id', 'executed_value', 'value', 'transact_time',
                                 'execution_type', 'order_qty', 'executed_qty', 'total_qty', 'side', 'visible_size',
                                 'order_id']
        data = read_messages
        window = Window(session_file=session_file)
        exe_type = ExecutionTypeStatic(session_file=session_file)

        for index, order_row in data.iterrows():
            order_id = order_row['order_id']
            visible_size = order_row['visible_size']
            side = order_row['side']
            total_qty = order_row['total_qty']
            executed_qty = order_row['executed_qty']
            order_qty = order_row['order_qty']
            execution_type = order_row['execution_type']
            transact_time = order_row['transact_time']
            value = order_row['value']
            executed_value = order_row['executed_value']
            broker_id = order_row['broker_id']
            instrument_id = order_row['instrument_id']  # set size attribute
            order = Order(order_id=order_id, visible_size=visible_size, side=side, total_qty=total_qty,
                          executed_qty=executed_qty
                          , order_qty=order_qty, execution_type=execution_type, transact_time=transact_time,
                          value=value, executed_value=executed_value
                          , broker_id=broker_id, instrument_id=instrument_id)

            #if order.value > 0:
            #self.normalize_data_frame = window.get_time_frame(order=order, time_delta=time_delta)
            window.get_all_attributes(order=order,time_delta=time_delta)
            exe_type.get_time_frame(order=order, time_delta=time_delta)
            if index == no_of_lines and no_of_lines != 0:
                break
        # print(self.normalize_data_frame)
        #self.normalize_df(writable_df=self.normalize_data_frame)
        #self.normalize_data_frame.to_csv("output/price_volume_average_static_normalize.csv", index=False,
                                       #  encoding='utf-8')

    def normalize_df(self, writable_df):
        mean_buy_price = self.normalize_data_frame['execute_order_buy_price'].mean()
        mean_sell_price = self.normalize_data_frame['execute_order_sell_price'].mean()
        mean_buy_volume = self.normalize_data_frame['execute_order_buy_volume'].mean()
        mean_sell_volume = self.normalize_data_frame['execute_order_sell_volume'].mean()

        std_buy_price = self.normalize_data_frame['execute_order_buy_price'].values.std(ddof=1)
        std_sell_price = self.normalize_data_frame['execute_order_sell_price'].values.std(ddof=1)
        std_buy_volume = self.normalize_data_frame['execute_order_buy_volume'].values.std(ddof=1)
        std_sell_volume = self.normalize_data_frame['execute_order_sell_volume'].values.std(ddof=1)

        print(mean_buy_price, mean_sell_price, std_buy_price, std_sell_price, mean_buy_volume, mean_sell_volume,
              std_buy_volume, std_sell_volume)

        self.normalize_data_frame['nom_exe_order_buy_price'] = (self.normalize_data_frame[
                                                                    'execute_order_buy_price'] - mean_buy_price) / std_buy_price
        self.normalize_data_frame['nom_exe_order_sell_price'] = (self.normalize_data_frame[
                                                                     'execute_order_sell_price'] - mean_sell_price) / std_sell_price
        self.normalize_data_frame['nom_exe_order_buy_volume'] = (self.normalize_data_frame[
                                                                     'execute_order_buy_volume'] - mean_buy_volume) / std_buy_volume
        self.normalize_data_frame['nom_exe_order_sell_volume'] = (self.normalize_data_frame[
                                                                      'execute_order_sell_volume'] - mean_sell_volume) / std_sell_volume
