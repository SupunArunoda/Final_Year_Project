from pandas import DataFrame, read_csv
from datetime import datetime
from dateutil import parser as DUp
import numpy as np
from matplotlib import pyplot as plt

from app.orderbook.Order import Order


class InterArrivalTime:
    def __init__(self):
        # session_file = 'E:\projects\Final_Year_Project\data\sessions.csv'
        # self.session = read_csv(session_file)
        # self.regular_list = self.get_regular_time()

        self.normalize_data_frame = DataFrame()

        self.sellNew = DataFrame()
        self.sellAmmend = DataFrame()
        self.sellCancel = DataFrame()
        self.sellExecute = DataFrame()
        self.buyNew = DataFrame()
        self.buyAmmend = DataFrame()
        self.buyCancel = DataFrame()
        self.buyExecute = DataFrame()
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

    def run_inter_arrival_time_static(self, message_file, time_delta):
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

            if order.execution_type == 0 and order.side == 2:
                if self.prevSellNew != 0:
                    diff = self.str_to_date_time(self.prevSellNew, order.transact_time)
                    self.sellNew = self.sellNew.append(DataFrame(
                        {
                            'inter_arr_time': diff,
                            'time_stamp': order.transact_time
                        }, index=[0]), ignore_index=True);

                    self.prevSellNew = order.transact_time
                else:
                    self.prevSellNew = order.transact_time

            if order.execution_type == 4 and order.side == 2:
                if self.prevSellAmmend != 0:
                    diff = self.str_to_date_time(self.prevSellAmmend, order.transact_time)
                    self.sellAmmend = self.sellAmmend.append(DataFrame(
                        {
                            'inter_arr_time': diff,
                            'time_stamp': order.transact_time
                        }, index=[0]), ignore_index=True);
                    self.prevSellAmmend = order.transact_time
                else:
                    self.prevSellAmmend = order.transact_time

            if order.execution_type == 5 and order.side == 2:
                if self.prevSellCancel != 0:
                    diff = self.str_to_date_time(self.prevSellCancel, order.transact_time)
                    self.sellCancel = self.sellCancel.append(DataFrame(
                        {
                            'inter_arr_time': diff,
                            'time_stamp': order.transact_time
                        }, index=[0]), ignore_index=True);
                    self.prevSellCancel = order.transact_time
                else:
                    self.prevSellCancel = order.transact_time

            if order.execution_type == 15 and order.side == 2:
                if self.prevSellExecute != 0:
                    diff = self.str_to_date_time(self.prevSellExecute, order.transact_time)
                    self.sellExecute = self.sellExecute.append(DataFrame(
                        {
                            'inter_arr_time': diff,
                            'time_stamp': order.transact_time
                        }, index=[0]), ignore_index=True);
                    self.prevSellExecute = order.transact_time
                else:
                    self.prevSellExecute = order.transact_time

            if order.execution_type == 0 and order.side == 1:
                if self.prevBuyNew != 0:
                    diff = self.str_to_date_time(self.prevBuyNew, order.transact_time)
                    self.buyNew = self.buyNew.append(DataFrame(
                        {
                            'inter_arr_time': diff,
                            'time_stamp': order.transact_time
                        }, index=[0]), ignore_index=True);
                    self.prevBuyNew = order.transact_time
                else:
                    self.prevBuyNew = order.transact_time

            if order.execution_type == 4 and order.side == 1:
                if self.prevBuyAmmend != 0:
                    diff = self.str_to_date_time(self.prevBuyAmmend, order.transact_time)
                    self.buyAmmend = self.buyAmmend.append(DataFrame(
                        {
                            'inter_arr_time': diff,
                            'time_stamp': order.transact_time
                        }, index=[0]), ignore_index=True);
                    self.prevBuyAmmend = order.transact_time
                else:
                    self.prevBuyAmmend = order.transact_time

            if order.execution_type == 5 and order.side == 1:
                if self.prevBuyCancel != 0:
                    diff = self.str_to_date_time(self.prevBuyCancel, order.transact_time)
                    self.buyCancel = self.buyCancel.append(DataFrame(
                        {
                            'inter_arr_time': diff,
                            'time_stamp': order.transact_time
                        }, index=[0]), ignore_index=True);
                    self.prevBuyCancel = order.transact_time
                else:
                    self.prevBuyCancel = order.transact_time

            if order.execution_type == 15 and order.side == 1:
                if self.prevBuyExecute != 0:
                    diff = self.str_to_date_time(self.prevBuyExecute, order.transact_time)
                    self.buyExecute = self.buyExecute.append(DataFrame(
                        {
                            'inter_arr_time': diff,
                            'time_stamp': order.transact_time
                        }, index=[0]), ignore_index=True);
                    self.prevBuyExecute = order.transact_time
                else:
                    self.prevBuyExecute = order.transact_time
        # print(self.sellNew)
        self.writeToFile()

    def writeToFile(self):
        # new sell orders
        mean_sell_new = np.mean(self.sellNew['inter_arr_time'], axis=0)
        std_sell_new = np.std(self.sellNew['inter_arr_time'], axis=0)
        self.sellNew['nom_inter_arr'] = (self.sellNew['inter_arr_time'] - mean_sell_new) / std_sell_new
        self.sellNew.to_csv(
            "../../output/inter_arrival_time/sell_new_inter_arrival_time.csv",
            index=False,
            encoding='utf-8')

        # executed sell orders
        mean_sell_execute = np.mean(self.sellExecute['inter_arr_time'], axis=0)
        std_sell_execute = np.std(self.sellExecute['inter_arr_time'], axis=0)
        self.sellExecute['nom_inter_arr'] = (self.sellExecute[
                                                 'inter_arr_time'] - mean_sell_execute) / std_sell_execute
        self.sellExecute.to_csv(
            "../../output/inter_arrival_time/sell_execute_inter_arrival_time.csv",
            index=False,
            encoding='utf-8')

        # cancelled sell orders
        mean_sell_cancel = np.mean(self.sellCancel['inter_arr_time'], axis=0)
        std_sell_cancel = np.std(self.sellCancel['inter_arr_time'], axis=0)
        self.sellCancel['nom_inter_arr'] = (self.sellCancel[
                                                'inter_arr_time'] - mean_sell_cancel) / std_sell_cancel
        self.sellCancel.to_csv(
            "../../output/inter_arrival_time/sell_cancel_inter_arrival_time.csv",
            index=False,
            encoding='utf-8')

        # ammended sell orders
        mean_sell_ammend = np.mean(self.sellAmmend['inter_arr_time'], axis=0)
        std_sell_ammend = np.std(self.sellAmmend['inter_arr_time'], axis=0)
        self.sellAmmend['nom_inter_arr'] = (self.sellAmmend[
                                                'inter_arr_time'] - mean_sell_ammend) / std_sell_ammend
        self.sellAmmend.to_csv(
            "../../output/inter_arrival_time/sell_ammend_inter_arrival_time.csv",
            index=False,
            encoding='utf-8')

        # new buy orders
        mean_buy_new = np.mean(self.buyNew['inter_arr_time'], axis=0)
        std_buy_new = np.std(self.buyNew['inter_arr_time'], axis=0)
        self.buyNew['nom_inter_arr'] = (self.buyNew[
                                            'inter_arr_time'] - mean_buy_new) / std_buy_new
        self.buyNew.to_csv(
            "../../output/inter_arrival_time/buy_new_inter_arrival_time.csv",
            index=False,
            encoding='utf-8')

        # ammended buy orders
        mean_buy_ammend = np.mean(self.buyAmmend['inter_arr_time'], axis=0)
        std_buy_ammend = np.std(self.buyAmmend['inter_arr_time'], axis=0)
        self.buyAmmend['nom_inter_arr'] = (self.buyAmmend[
                                               'inter_arr_time'] - mean_buy_ammend) / std_buy_ammend
        self.buyAmmend.to_csv(
            "../../output/inter_arrival_time/buy_ammend_inter_arrival_time.csv",
            index=False,
            encoding='utf-8')

        # cancel buy orders
        mean_buy_cancel = np.mean(self.buyCancel['inter_arr_time'], axis=0)
        std_buy_cancel = np.std(self.buyCancel['inter_arr_time'], axis=0)
        self.buyCancel['nom_inter_arr'] = (self.buyCancel[
                                               'inter_arr_time'] - mean_buy_cancel) / std_buy_cancel
        self.buyCancel.to_csv(
            "../../output/inter_arrival_time/buy_cancel_inter_arrival_time.csv",
            index=False,
            encoding='utf-8')

        # executed buy orders
        mean_buy_execute = np.mean(self.buyExecute['inter_arr_time'], axis=0)
        std_buy_execute = np.std(self.buyExecute['inter_arr_time'], axis=0)
        self.buyExecute['nom_inter_arr'] = (self.buyExecute[
                                                'inter_arr_time'] - mean_buy_execute) / std_buy_execute
        self.buyExecute.to_csv(
            "../../output/inter_arrival_time/buy_executed_inter_arrival_time.csv",
            index=False,
            encoding='utf-8')

        # X = self.sellNew['nom_inter_arr']
        # X = X.values
        #
        # x = X[:, 0]
        # y = np.array(range(1, len(X) + 1))
        #
        # plt.plot(y, x)
        # plt.show()

    def plotHistogram(self):
        df = read_csv('../../output/inter_arrival_time/buy_executed_inter_arrival_time.csv')
        df = df['nom_inter_arr'][0:1000]
        X = df.values

        x = X[0:]
        y = np.array(range(1, len(X) + 1))

        plt.plot(y, x)
        plt.show()

# InterArrivalTime().run_inter_arrival_time_static(message_file='../../data/data.csv')
InterArrivalTime().plotHistogram()
