from pandas import DataFrame, read_csv
import datetime
import csv
import numpy as np
from dateutil import parser as DUp

from app.orderbook.OrderBook import OrderBook
from app.preprocess.window.TimeWindow import TimeWindow


class OrderbookSimulation:
    def __init__(self, session_file, window):

        self.attributes = DataFrame()
        self.fileCounter = 0
        self.temp_time = 0;
        self.volume_average_list = []
        self.detailsList = [0 for _ in range(7)]

        self.session = session_file
        self.regular_list = self.get_regular_time()
        # self.window = TimeWindow(no_of_events=no_of_events)
        self.window = window
        self.smallWindow = TimeWindow(time_delta=30)

        # read_messages = read_csv(data_file, header=None)
        self.orderbook = OrderBook()
        self.details = []

    def get_regular_time(self):
        count = 0;
        reg_list = []
        for index, session_row in self.session.iterrows():
            session_name = session_row['session_name']
            if (session_name[:15] == 'Regular Trading'):
                reg_list.insert(count, DUp.parse(session_row['transact_time']))
                count += 1
        return reg_list

    def get_time_frame(self, order,row_val):
        self.details = self.orderbook.processOrder(order=order)
        # const_time_gap=datetime.timedelta(0, time_delta)#set time window value
        temp_trasact_time = DUp.parse(order.transact_time)
        for i in range(0, len(self.regular_list), 2):
            if (temp_trasact_time >= self.regular_list[i] and temp_trasact_time <= self.regular_list[i + 1]):
                if (self.window.isWindowLimitReach(order=order) == False):
                    if (self.smallWindow.isWindowLimitReach(order=order) == False):
                        self.check_order(order=order)
                        if (self.temp_time == 0):
                            self.temp_time = temp_trasact_time

                    else:
                        self.check_order(order=order)

                        index = str(self.temp_time) + str('$$') + str(order.transact_time)
                        self.volume_average_list.append(index)
                        self.attributes = self.attributes.append(DataFrame(
                            {'time_index': self.volume_average_list[0],
                             'best_bid': self.detailsList[0],
                             'best_ask': self.detailsList[1],
                             'top_buy_price_points': self.detailsList[5],
                             'top_sell_price_points': self.detailsList[6]
                             }, index=[0]), ignore_index=True);

                        self.remove_values()
                        self.temp_time = 0
                        if (self.temp_time == 0):
                            self.temp_time = temp_trasact_time

                else:
                    self.fileCounter += 1
                    self.attributes.to_csv("app/output/"+str(row_val)+"_orderbook_simulation_" + str(self.fileCounter) + ".csv",
                                           index=False,
                                           encoding='utf-8')

                    self.attributes = DataFrame()

        return self.attributes;

    def check_order(self, order):
        self.detailsList[0] = self.details[0]
        self.detailsList[1] = self.details[1]
        self.detailsList[2] += self.details[2]
        self.detailsList[3] += self.details[3]
        self.detailsList[4] += 1
        self.detailsList[5] = self.details[4]
        self.detailsList[6] = self.details[5]

    def remove_values(self):
        self.volume_average_list = []
        self.detailsList = [0 for _ in range(7)]
