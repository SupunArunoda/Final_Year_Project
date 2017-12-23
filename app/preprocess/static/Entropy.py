from pandas import DataFrame, read_csv
from datetime import datetime
from dateutil import parser as DUp
import numpy as np
import math

from app.orderbook.Order import Order

#Entropy clauclation for order by events
class Entropy:
    def __init__(self, session_file, window):
        self.temp_time = 0
        self.session = session_file
        self.regular_list = self.get_regular_time()
        self.final_dataframe = DataFrame()
        self.attributes = DataFrame()
        self.type_df = []
        self.side_df = []
        self.start_times = []
        self.end_times = []
        self.window = window
        self.chunk = []
        # print(self.regular_list)

    #get only regular time list
    def get_regular_time(self):
        count = 0;
        reg_list = []
        for index, session_row in self.session.iterrows():
            session_name = session_row['session_name']
            if (session_name[:15] == 'Regular Trading'):
                reg_list.insert(count, DUp.parse(session_row['transact_time']))
                count += 1
        return reg_list

    def get_entropy(self, order):
        temp_trasact_time = DUp.parse(order.transact_time)
        for i in range(0, len(self.regular_list), 2):
            if (temp_trasact_time >= self.regular_list[i] and temp_trasact_time <= self.regular_list[i + 1]):
                if (self.window.isWindowLimitReach(order=order) == False):
                    self.chunk.append(order)
                    if (self.temp_time == 0):
                        self.temp_time = temp_trasact_time
                else:
                    self.chunk.append(order)
                    self.calculate_entropy(self.chunk)

                    index = str(self.temp_time) + str('$$') + str(order.transact_time)
                    self.attributes = self.attributes.append(DataFrame(
                        {'time_index': index,
                         'entropy_exec_type': self.type_df,
                         'entropy_side': self.side_df
                         }, index=[0]), ignore_index=True);

                    self.type_df = []
                    self.side_df = []
                    self.start_times = []
                    self.end_times = []
                    self.final_dataframe = DataFrame()
                    self.temp_time = temp_trasact_time
        return self.attributes

    def calculate_entropy(self, chunk):
        newC, ammendC, cancelC, execC = 0, 0, 0, 0
        sellC, buyC = 0, 0
        for i in range(0, len(chunk)):
            order = chunk[i]
            if order.side == 1:
                buyC += 1
            if order.side == 2:
                sellC += 1
            if order.execution_type == 0:
                newC += 1
            if order.execution_type == 4:
                ammendC += 1
            if order.execution_type == 5:
                cancelC += 1
            if order.execution_type == 15:
                execC += 1

        type_total = len(chunk)
        type_entropy = -(newC / type_total) * math.log2(newC / type_total) - (ammendC / type_total) * math.log2(
            ammendC / type_total) - (cancelC / type_total) * math.log2(cancelC / type_total) + (execC / type_total) * math.log2(
            execC / type_total)

        side_total = sellC + buyC
        side_entropy = -(sellC / side_total) * math.log2(sellC / side_total) - (buyC / side_total) * math.log2(
            buyC / side_total)

        self.type_df.append(type_entropy)
        self.side_df.append(side_entropy)


