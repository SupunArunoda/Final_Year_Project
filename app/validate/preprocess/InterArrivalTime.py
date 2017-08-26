from pandas import DataFrame, read_csv
from datetime import datetime
from dateutil import parser as DUp
import numpy as np
from orderbook.Order import Order


class InterArrivalTime:
    def __init__(self):
        # session_file = 'E:\projects\Final_Year_Project\data\sessions.csv'
        # self.session = read_csv(session_file)
        # self.regular_list = self.get_regular_time()

        self.normalize_data_frame = DataFrame()

        self.sellNew = []
        self.sellAmmend = []
        self.sellCancel = []
        self.sellExecute = []
        self.buyNew = []
        self.buyAmmend = []
        self.buyCancel = []
        self.buyExecute = []
        self.prevSellNew = 0
        self.prevSellAmmend = 0
        self.prevSellCancel = 0
        self.prevSellExecute = 0
        self.prevBuyNew = 0
        self.prevBuyAmmend = 0
        self.prevBuyCancel = 0
        self.prevBuyExecute = 0

    def get_regular_time(self):
        count = 0;
        reg_list = []
        for index, session_row in self.session.iterrows():
            session_name = session_row['session_name']
            if (session_name[:15] == 'Regular Trading'):
                reg_list.insert(count, DUp.parse(session_row['transact_time']))
                count += 1
        return reg_list

    def str_to_date_time(self, str_date_1, str_date_2):
        new_date_1 = datetime.strptime(str_date_1, '%Y-%m-%d %H:%M:%S.%f')
        new_date_2 = datetime.strptime(str_date_2, '%Y-%m-%d %H:%M:%S.%f')
        diff = ((new_date_2 - new_date_1).seconds) / 60
        return diff

    def run_inter_arrival_time_static(self, message_file):

        read_messages = read_csv(message_file, header=None)
        read_messages.columns = ['instrument_id', 'broker_id', 'executed_value', 'value', 'transact_time',
                                 'execution_type', 'order_qty', 'executed_qty', 'total_qty', 'side', 'visible_size',
                                 'order_id']
        data = read_messages

        for index, order_row in data.iterrows():
            if index == 0:
                continue

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

            if order.execution_type == '0' and order.side == '2':
                if self.prevSellNew != 0:
                    diff = self.str_to_date_time(self.prevSellNew, order.transact_time)
                    self.sellNew.append(diff)
                    self.prevSellNew = order.transact_time
                else:
                    self.prevSellNew = order.transact_time

            if order.execution_type == '4' and order.side == '2':
                if self.prevSellAmmend != 0:
                    diff = self.str_to_date_time(self.prevSellAmmend, order.transact_time)
                    self.sellAmmend.append(diff)
                    self.prevSellAmmend = order.transact_time
                else:
                    self.prevSellAmmend = order.transact_time

            if order.execution_type == '5' and order.side == '2':
                if self.prevSellCancel != 0:
                    diff = self.str_to_date_time(self.prevSellCancel, order.transact_time)
                    self.sellCancel.append(diff)
                    self.prevSellCancel = order.transact_time
                else:
                    self.prevSellCancel = order.transact_time

            if order.execution_type == '15' and order.side == '2':
                if self.prevSellExecute != 0:
                    diff = self.str_to_date_time(self.prevSellExecute, order.transact_time)
                    self.sellExecute.append(diff)
                    self.prevSellExecute = order.transact_time
                else:
                    self.prevSellExecute = order.transact_time

            if order.execution_type == '0' and order.side == '1':
                if self.prevBuyNew != 0:
                    diff = self.str_to_date_time(self.prevBuyNew, order.transact_time)
                    self.buyNew.append(diff)
                    self.prevBuyNew = order.transact_time
                else:
                    self.prevBuyNew = order.transact_time

            if order.execution_type == '4' and order.side == '1':
                if self.prevBuyAmmend != 0:
                    diff = self.str_to_date_time(self.prevBuyAmmend, order.transact_time)
                    self.buyAmmend.append(diff)
                    self.prevBuyAmmend = order.transact_time
                else:
                    self.prevBuyAmmend = order.transact_time

            if order.execution_type == '5' and order.side == '1':
                if self.prevBuyCancel != 0:
                    diff = self.str_to_date_time(self.prevBuyCancel, order.transact_time)
                    self.buyCancel.append(diff)
                    self.prevBuyCancel = order.transact_time
                else:
                    self.prevBuyCancel = order.transact_time

            if order.execution_type == '15' and order.side == '1':
                if self.prevBuyExecute != 0:
                    diff = self.str_to_date_time(self.prevBuyExecute, order.transact_time)
                    self.buyExecute.append(diff)
                    self.prevBuyExecute = order.transact_time
                else:
                    self.prevBuyExecute = order.transact_time

        print(self.sellExecute)

    # def normalize_df(self, writable_df):
        # mean_sell_new = np.mean(writable_df, axis=0)
        # mean_sell_ammend = self.sellAmmend.mean()
        # mean_buy_cancel = self.sellCancel.mean()
        # mean_sell_execute = self.sellExecute.mean()
        # mean_buy_new = self.buyNew.mean()
        # mean_buy_ammend = self.buyAmmend.mean()
        # mean_buy_cancel = self.buyCancel.mean()
        # mean_buy_execute = self.buyExecute.mean()

        # std_sell_new = np.std(self.sellNew, axis=0)
        # std_sell_ammend = self.sellAmmend.values.std(ddof=1)
        # std_buy_cancel = self.sellCancel.values.std(ddof=1)
        # std_sell_execute = self.sellExecute.values.std(ddof=1)
        # std_buy_new = self.buyNew.values.std(ddof=1)
        # std_buy_ammend = self.buyAmmend.values.std(ddof=1)
        # std_buy_cancel = self.buyCancel.values.std(ddof=1)
        # std_buy_execute = self.buyExecute.values.std(ddof=1)

        # self.normalize_data_frame['new_sell'] = (self.sellNewDf['sellNew'] - mean_sell_new) / std_sell_new
        # self.normalize_data_frame['ammend_sell'] = (self.normalize_data_frame[
        #                                                 'execute_order_sell_price'] - mean_sell_price) / std_sell_price
        # self.normalize_data_frame['cancel_sell'] = (self.normalize_data_frame[
        #                                                 'execute_order_buy_volume'] - mean_buy_volume) / std_buy_volume
        # self.normalize_data_frame['execute_sell'] = (self.normalize_data_frame[
        #                                                  'execute_order_sell_volume'] - mean_sell_volume) / std_sell_volume


InterArrivalTime().run_inter_arrival_time_static(message_file='E:\projects\Final_Year_Project\data\data.csv')
