from app.orderbook.Order import Order
from app.orderbook.OrderBook import OrderBook
from pandas import read_csv
from app.db.PreprocessFile import PreprocessFile
from app.db.PreprocessFileController import PreprocessFileController
from app.preprocess.static.PriceVolumeAverage import Window
from pandas import DataFrame, read_csv
from app.preprocess.window.TimeWindow import TimeWindow
from app.preprocess.window.EventWindow import EventWindow
from app.preprocess.static.ExecutionTypeStatic import ExecutionTypeStatic
from app.preprocess.static.PriceGapStatic import PriceGapStatic
from app.preprocess.static.Entropy import Entropy
import numpy as np
from time import gmtime, strftime

class AllAttribute:
    def __init__(self):
        self.price_data_frame = DataFrame()
        self.exe_type_data_frame=DataFrame()
        self.entropy_data_frame=DataFrame()

    def run(self, message_file, session_file,type,size):

        uploaded_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        output_path = "app/output/"
        last_process_start = strftime("%Y-%m-%d %H:%M:%S", gmtime())

        # read_messages = read_csv(message_file, header=None)
        # read_messages.columns = ['instrument_id', 'broker_id', 'executed_value', 'value', 'transact_time','execution_type', 'order_qty', 'executed_qty', 'total_qty', 'side', 'visible_size','order_id']
        data = read_csv("app/data/data.csv")
        if(type=="time"):
            price_window=TimeWindow(time_delta=size)
            ex_type_window=TimeWindow(time_delta=size)
            price_gap_window=TimeWindow(time_delta=size)
            entropy_window=TimeWindow(time_delta=size)
        else:
            price_window = EventWindow(no_of_events=size)
            ex_type_window = EventWindow(no_of_events=size)
            price_gap_window = EventWindow(no_of_events=size)
            entropy_window = EventWindow(no_of_events=size)
        price_volume = Window(session_file=session_file,window=price_window)
        exe_type=ExecutionTypeStatic(session_file=session_file,window=ex_type_window)
        price_gap=PriceGapStatic(session_file=session_file,window=price_gap_window)
        entropy = Entropy(session_file=session_file,window=entropy_window)

        return_data = {}
        pfc = PreprocessFileController()
        row_val=pfc.getMaximumValue()+1

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
            if order.value>0:
                self.price_data_frame = price_volume.get_time_frame(order=order)
                self.exe_type_data_frame=exe_type.get_time_frame(order=order)
                price_gap.get_regular_gap_chunks(order=order,row_val=row_val)
                self.entropy_data_frame = entropy.get_entropy(order=order)

        last_process_end = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        input_file = "app/data/data.csv"
        output_file = output_path
        pf = PreprocessFile(input_file=input_file, uploaded_time=uploaded_time, last_process_start=last_process_start,
                            last_process_end=last_process_end, output_file=output_file)

        return_data['proprocess_index'] = pfc.saveProcessFile(pf)

        self.normalize_price()
        self.normalize_exe_type()
        self.exe_type_data_frame.to_csv(output_path+str(row_val)+"_exe_type.csv", index=False,
                                         encoding='utf-8')
        self.price_data_frame.to_csv(output_path+str(row_val)+"_price_vol.csv", index=False,
                                         encoding='utf-8')
        self.entropy_data_frame.to_csv(output_path+str(row_val)+"_entropy.csv", index=False,
                                     encoding='utf-8')
        # print(self.entropy_data_frame)
        return_data['total_rows'] = len(data)
        return return_data

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

    def normalize_exe_type(self):
        mean_buy_execute = self.exe_type_data_frame['execute_order_buy_average'].mean()
        mean_sell_execute = self.exe_type_data_frame['execute_order_sell_average'].mean()
        mean_buy_new = self.exe_type_data_frame['new_order_buy_average'].mean()
        mean_sell_new = self.exe_type_data_frame['new_order_sell_average'].mean()
        mean_buy_ammend = self.exe_type_data_frame['ammend_order_buy_average'].mean()
        mean_sell_ammend = self.exe_type_data_frame['ammend_order_sell_average'].mean()
        mean_buy_cancel = self.exe_type_data_frame['cancel_order_buy_average'].mean()
        mean_sell_cancel = self.exe_type_data_frame['cancel_order_sell_average'].mean()

        mean_execute = self.exe_type_data_frame['execute_order_average'].mean()
        mean_new = self.exe_type_data_frame['new_order_average'].mean()
        mean_cancel = self.exe_type_data_frame['cancel_order_average'].mean()
        mean_ammend = self.exe_type_data_frame['ammend_order_average'].mean()

        std_buy_execute = self.exe_type_data_frame['execute_order_buy_average'].values.std(ddof=1)
        std_sell_execute = self.exe_type_data_frame['execute_order_sell_average'].values.std(ddof=1)
        std_buy_new = self.exe_type_data_frame['new_order_buy_average'].values.std(ddof=1)
        std_sell_new = self.exe_type_data_frame['new_order_sell_average'].values.std(ddof=1)
        std_buy_ammend = self.exe_type_data_frame['ammend_order_buy_average'].values.std(ddof=1)
        std_sell_ammend = self.exe_type_data_frame['ammend_order_sell_average'].values.std(ddof=1)
        std_buy_cancel = self.exe_type_data_frame['cancel_order_buy_average'].values.std(ddof=1)
        std_sell_cancel = self.exe_type_data_frame['cancel_order_sell_average'].values.std(ddof=1)

        std_execute = self.exe_type_data_frame['execute_order_average'].values.std(ddof=1)
        std_new = self.exe_type_data_frame['new_order_average'].values.std(ddof=1)
        std_cancel = self.exe_type_data_frame['cancel_order_average'].values.std(ddof=1)
        std_ammend = self.exe_type_data_frame['ammend_order_average'].values.std(ddof=1)

        print(mean_buy_execute, std_buy_execute, mean_sell_ammend, std_sell_ammend)

        self.exe_type_data_frame['nom_exe_buy'] = (self.exe_type_data_frame[
                                                        'execute_order_buy_average'] - mean_buy_execute) / std_buy_execute
        self.exe_type_data_frame['nom_exe_sell'] = (self.exe_type_data_frame[
                                                         'execute_order_sell_average'] - mean_sell_execute) / std_sell_execute
        self.exe_type_data_frame['nom_new_buy'] = (self.exe_type_data_frame[
                                                        'new_order_buy_average'] - mean_buy_new) / std_buy_new
        self.exe_type_data_frame['nom_new_sell'] = (self.exe_type_data_frame[
                                                         'new_order_sell_average'] - mean_sell_new) / std_sell_new

        self.exe_type_data_frame['nom_amm_buy'] = (self.exe_type_data_frame[
                                                        'ammend_order_buy_average'] - mean_buy_ammend) / std_buy_ammend
        self.exe_type_data_frame['nom_amm_sell'] = (self.exe_type_data_frame[
                                                         'ammend_order_sell_average'] - mean_sell_ammend) / std_sell_ammend
        self.exe_type_data_frame['nom_can_buy'] = (self.exe_type_data_frame[
                                                        'cancel_order_buy_average'] - mean_buy_cancel) / std_buy_cancel
        self.exe_type_data_frame['nom_can_sell'] = (self.exe_type_data_frame[
                                                         'cancel_order_sell_average'] - mean_sell_cancel) / std_sell_cancel

        self.exe_type_data_frame['nom_exe'] = (self.exe_type_data_frame[
                                                    'execute_order_average'] - mean_execute) / std_execute
        self.exe_type_data_frame['nom_new'] = (self.exe_type_data_frame['new_order_average'] - mean_new) / std_new
        self.exe_type_data_frame['nom_can'] = (self.exe_type_data_frame[
                                                    'cancel_order_average'] - mean_cancel) / std_cancel
        self.exe_type_data_frame['nom_amm'] = (self.exe_type_data_frame[
                                                    'ammend_order_average'] - mean_ammend) / std_ammend
