from app.orderbook.Order import Order
from app.orderbook.OrderBook import OrderBook
from pandas import read_csv
from app.preprocess.static.PriceVolumeAverage import Window
from pandas import DataFrame, read_csv
from app.preprocess.window.TimeWindow import TimeWindow
from app.preprocess.static.ExecutionTypeStatic import ExecutionTypeStatic
import numpy as np


class AllAttribute:
    def __init__(self):
        self.price_data_frame = DataFrame()
        self.exe_type_data_frame=DataFrame()

    def run(self, message_file, session_file, no_of_lines, window):

        read_messages = read_csv(message_file, header=None)
        read_messages.columns = ['instrument_id', 'broker_id', 'executed_value', 'value', 'transact_time',
                                 'execution_type', 'order_qty', 'executed_qty', 'total_qty', 'side', 'visible_size',
                                 'order_id']
        data = read_messages

        time_window_1 = TimeWindow(time_delta=1200)
        time_window_2 = TimeWindow(time_delta=1200)
        price_volume = Window(session_file=session_file,window=time_window_1)
        exe_type=ExecutionTypeStatic(session_file=session_file,window=time_window_2)

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

            if order.value > 0:
                self.price_data_frame = price_volume.get_time_frame(order=order)
                self.exe_type_data_frame=exe_type.get_time_frame(order=order)
            if index == no_of_lines and no_of_lines != 0:
                break
        # print(self.normalize_data_frame)
        self.normalize_price()
        self.exe_type_data_frame.to_csv("app/output/exe_type.csv", index=False,
                                         encoding='utf-8')
        self.price_data_frame.to_csv("app/output/price_vol.csv", index=False,
                                         encoding='utf-8')
        # merged = self.price_data_frame.merge(self.exe_type_data_frame, on='time_index')
        # merged.to_csv("/app/output/all.csv", index=False,
        #                                  encoding='utf-8')

    def normalize_price(self):
        mean_buy_price = self.price_data_frame['execute_order_buy_price'].mean()
        mean_sell_price = self.price_data_frame['execute_order_sell_price'].mean()
        mean_buy_volume = self.price_data_frame['execute_order_buy_volume'].mean()
        mean_sell_volume = self.price_data_frame['execute_order_sell_volume'].mean()

        std_buy_price = self.price_data_frame['execute_order_buy_price'].values.std(ddof=1)
        std_sell_price = self.price_data_frame['execute_order_sell_price'].values.std(ddof=1)
        std_buy_volume = self.price_data_frame['execute_order_buy_volume'].values.std(ddof=1)
        std_sell_volume = self.price_data_frame['execute_order_sell_volume'].values.std(ddof=1)

        print(mean_buy_price, mean_sell_price, std_buy_price, std_sell_price, mean_buy_volume, mean_sell_volume,
              std_buy_volume, std_sell_volume)

        self.price_data_frame['nom_exe_order_buy_price'] = (self.price_data_frame[
                                                                    'execute_order_buy_price'] - mean_buy_price) / std_buy_price
        self.price_data_frame['nom_exe_order_sell_price'] = (self.price_data_frame[
                                                                     'execute_order_sell_price'] - mean_sell_price) / std_sell_price
        self.price_data_frame['nom_exe_order_buy_volume'] = (self.price_data_frame[
                                                                     'execute_order_buy_volume'] - mean_buy_volume) / std_buy_volume
        self.price_data_frame['nom_exe_order_sell_volume'] = (self.price_data_frame[
                                                                      'execute_order_sell_volume'] - mean_sell_volume) / std_sell_volume

    def normalize_ex_type(self):
        mean_ammend = self.price_data_frame['execute_order_buy_price'].mean()
        mean_sell_price = self.price_data_frame['execute_order_sell_price'].mean()
        mean_buy_volume = self.price_data_frame['execute_order_buy_volume'].mean()
        mean_sell_volume = self.price_data_frame['execute_order_sell_volume'].mean()

        std_buy_price = self.price_data_frame['execute_order_buy_price'].values.std(ddof=1)
        std_sell_price = self.price_data_frame['execute_order_sell_price'].values.std(ddof=1)
        std_buy_volume = self.price_data_frame['execute_order_buy_volume'].values.std(ddof=1)
        std_sell_volume = self.price_data_frame['execute_order_sell_volume'].values.std(ddof=1)


        self.price_data_frame['nom_exe_order_buy_price'] = (self.price_data_frame[
                                                                'execute_order_buy_price'] - mean_buy_price) / std_buy_price
        self.price_data_frame['nom_exe_order_sell_price'] = (self.price_data_frame[
                                                                 'execute_order_sell_price'] - mean_sell_price) / std_sell_price
        self.price_data_frame['nom_exe_order_buy_volume'] = (self.price_data_frame[
                                                                 'execute_order_buy_volume'] - mean_buy_volume) / std_buy_volume
        self.price_data_frame['nom_exe_order_sell_volume'] = (self.price_data_frame[
                                                                  'execute_order_sell_volume'] - mean_sell_volume) / std_sell_volume



