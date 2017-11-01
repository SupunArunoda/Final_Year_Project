from pandas import DataFrame,read_csv
import datetime
import csv
from dateutil import parser as DUp
import numpy as np

from app.preprocess.window.TimeWindow import TimeWindow


class ExecutionTypeStatic:


    def __init__(self,session_file, window):

        self.attributes = DataFrame()
        self.temp_time=0;

        self.count_order_type_list = [[0 for _ in range(2)] for _ in range(4)]
        self.count_list=[]
        self.session = read_csv(session_file)
        self.regular_list=self.get_regular_time()

        # self.window = TimeWindow(time_delta=1200)
        self.window = window


    def get_regular_time(self):
        count=0;
        reg_list=[]
        for index,session_row in self.session.iterrows():
            session_name=session_row['session_name']
            if(session_name[:15]=='Regular Trading'):
                reg_list.insert(count,DUp.parse(session_row['transact_time']))
                count+=1
        return reg_list

    # def get_time_frame(self,order,time_delta):
    #     const_time_gap=datetime.timedelta(0, time_delta)#set time window value
    #     temp_trasact_time=DUp.parse(order.transact_time)
    #     for i in range(0,len(self.regular_list),2):
    #         if(temp_trasact_time>=self.regular_list[i] and temp_trasact_time <= self.regular_list[i + 1]):
    #             if (self.temp_time != 0):
    #                 time_gap=temp_trasact_time-self.temp_time;
    #                 if(time_gap<=const_time_gap):
    #                     self.check_order_type(order=order)
    #                 else:
    #                     self.check_order_type(order=order)
    #
    #                     index=str(self.temp_time)+str('$$')+str(order.transact_time)
    #                     self.count_list.append(index)
    #                     self.get_all_count_average()
    #                     if (self.count_list[2] != 0 and self.count_list[4] != 0 and self.count_list[6] != 0):
    #                         self.attributes = self.attributes.append(DataFrame(
    #                             {'time_index_volume': self.count_list[0],
    #                              'new_order_buy_average': self.count_list[1],
    #                              'new_order_sell_average': self.count_list[2],
    #                              'cancel_order_buy_average': self.count_list[3],
    #                              'cancel_order_sell_average': self.count_list[4],
    #                              'execute_order_buy_average': self.count_list[5],
    #                              'execute_order_sell_average': self.count_list[6],
    #                              'ammend_order_buy_average': self.count_list[7],
    #                              'ammend_order_sell_average': self.count_list[8],
    #                              'new_order_average': round((self.count_list[1] / self.count_list[2]), 4),
    #                              'execute_order_average': round((self.count_list[5] / self.count_list[6]), 4),
    #                              'cancel_order_average': round((self.count_list[3] / self.count_list[4]), 4),
    #                              'ammend_order_average': round((self.count_list[7] / self.count_list[8]), 4)
    #                              }, index=[0]), ignore_index=True);
    #                     else:
    #                         self.attributes = self.attributes.append(DataFrame(
    #                             {'time_index_volume': self.count_list[0],
    #                              'new_order_buy_average': self.count_list[1],
    #                              'new_order_sell_average': self.count_list[2],
    #                              'cancel_order_buy_average': self.count_list[3],
    #                              'cancel_order_sell_average': self.count_list[4],
    #                              'execute_order_buy_average': self.count_list[5],
    #                              'execute_order_sell_average': self.count_list[6],
    #                              'ammend_order_buy_average': self.count_list[7],
    #                              'ammend_order_sell_average': self.count_list[8],
    #                              'new_order_average': 0,
    #                              'execute_order_average': 0,
    #                              'cancel_order_average': 0,
    #                              'ammend_order_average': 0
    #                              }, index=[0]), ignore_index=True);
    #                     self.remove_values()
    #                     self.temp_time=0
    #                 if(self.temp_time==0):
    #                     self.temp_time = temp_trasact_time
    #
    #             elif(self.temp_time==0):
    #                 self.temp_time=temp_trasact_time
    #                 self.check_order_type(order=order)
    #
    #     return self.attributes;

    def get_time_frame(self,order,time_delta):
        const_time_gap=datetime.timedelta(0, time_delta)#set time window value
        temp_trasact_time=DUp.parse(order.transact_time)
        for i in range(0,len(self.regular_list),2):
            if(temp_trasact_time>=self.regular_list[i] and temp_trasact_time <= self.regular_list[i + 1]):
                if (self.window.isWindowLimitReach(order=order) == False):
                    # time_gap=temp_trasact_time-self.temp_time;
                    self.check_order_type(order=order)
                    if (self.temp_time == 0):
                        self.temp_time = temp_trasact_time

                else:
                    self.check_order_type(order=order)

                    index=str(self.temp_time)+str('$$')+str(order.transact_time)
                    self.count_list.append(index)
                    self.get_all_count_average()
                    if (self.count_list[2] != 0 and self.count_list[4] != 0 and self.count_list[6] != 0):
                        self.attributes = self.attributes.append(DataFrame(
                            {'time_index_volume': self.count_list[0],
                             'new_order_buy_average': self.count_list[1],
                             'new_order_sell_average': self.count_list[2],
                             'cancel_order_buy_average': self.count_list[3],
                             'cancel_order_sell_average': self.count_list[4],
                             'execute_order_buy_average': self.count_list[5],
                             'execute_order_sell_average': self.count_list[6],
                             'ammend_order_buy_average': self.count_list[7],
                             'ammend_order_sell_average': self.count_list[8],
                             'new_order_average': round((self.count_list[1] / self.count_list[2]), 4),
                             'execute_order_average': round((self.count_list[5] / self.count_list[6]), 4),
                             'cancel_order_average': round((self.count_list[3] / self.count_list[4]), 4),
                             'ammend_order_average': round((self.count_list[7] / self.count_list[8]), 4)
                             }, index=[0]), ignore_index=True);
                    else:
                        self.attributes = self.attributes.append(DataFrame(
                            {'time_index_volume': self.count_list[0],
                             'new_order_buy_average': self.count_list[1],
                             'new_order_sell_average': self.count_list[2],
                             'cancel_order_buy_average': self.count_list[3],
                             'cancel_order_sell_average': self.count_list[4],
                             'execute_order_buy_average': self.count_list[5],
                             'execute_order_sell_average': self.count_list[6],
                             'ammend_order_buy_average': self.count_list[7],
                             'ammend_order_sell_average': self.count_list[8],
                             'new_order_average': 0,
                             'execute_order_average': 0,
                             'cancel_order_average': 0,
                             'ammend_order_average': 0
                             }, index=[0]), ignore_index=True);
                    self.remove_values()
                    self.temp_time=0
                if(self.temp_time==0):
                    self.temp_time = temp_trasact_time

        return self.attributes;

    def check_order_type(self,order):
        if order.execution_type==0:#new order check
            self.count_order_type(order=order, type=0)
        elif order.execution_type==4:#cancel order check
            self.count_order_type(order=order, type=1)
        elif order.execution_type == 15:#execution order
            self.count_order_type(order=order, type=2)
        elif order.execution_type == 5:#ammend order
            self.count_order_type(order=order, type=3)

    def count_order_type(self,order,type):
        if (order.side == 1):#buy order check
            self.count_order_type_list[type][0]+=1

        elif (order.side == 2):#sell order check
            self.count_order_type_list[type][1] += 1

    def get_all_count_average(self):
        col_list=[sum(x) for x in zip(*self.count_order_type_list)]#get column sum
        for i in range(len(self.count_order_type_list)):
            for j in range(len(self.count_order_type_list[i])):
                if(col_list[j]!=0):
                    temp_average=self.count_order_type_list[i][j]/col_list[j]
                    self.count_list.append(round(temp_average,4))
                else:
                    self.count_list.append(float(0))

    def remove_values(self):
        self.count_order_type_list = [[0 for _ in range(2)] for _ in range(4)]
        self.count_list = []
