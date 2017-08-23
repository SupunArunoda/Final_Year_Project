from pandas import DataFrame,read_csv
import datetime
import csv
from dateutil import parser as DUp
import numpy as np
from itertools import tee

class ExecutionTypeDynamic:


    def __init__(self,session_file):

        self.attributes = DataFrame()
        self.temp_time=0;
        self.slide_window_flag=True
        self.lag_orders=[]

        self.count_order_type_list = [[0 for _ in range(2)] for _ in range(4)]
        self.count_list=[]
        self.session = read_csv(session_file)
        self.regular_list=self.get_regular_time()


    def get_regular_time(self):
        count=0;
        reg_list=[]
        for index,session_row in self.session.iterrows():
            session_name=session_row['session_name']
            if(session_name[:15]=='Regular Trading'):
                reg_list.insert(count,DUp.parse(session_row['transact_time']))
                count+=1
        return reg_list

    def sliding_window(self,iterable,size):
        iters = tee(iterable, size)
        for i in range(1, size):
            for each in iters[i:]:
                next(each, None)
        return zip(*iters)


    def get_time_frame(self,order,time_delta,time_lag):
        const_time_gap=datetime.timedelta(0, time_delta)#set time window value
        temp_trasact_time=DUp.parse(order.transact_time)

        for i in range(0,len(self.regular_list),2):
            if(temp_trasact_time>=self.regular_list[i] and temp_trasact_time<=self.regular_list[i+1]):
                if(self.temp_time!=0):
                    time_gap=temp_trasact_time-self.temp_time;
                    dynamic_valid=time_gap+time_lag

                    if(time_gap<=const_time_gap):
                        self.check_order_type(order=order)
                    else:
                        self.check_order_type(order=order)

                        index=str(self.temp_time)+str('$$')+str(order.transact_time)
                        self.count_list.append(index)
                        self.get_all_count_average()

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

                             }, index=[0]), ignore_index=True);

                        self.remove_values()
                        self.temp_time=0
                        self.slide_window_flag=False# start the next window
                    if(dynamic_valid>=const_time_gap & self.slide_window_flag):
                        self.lag_orders.append(order)


                    if(self.temp_time==0):
                        self.temp_time = temp_trasact_time

                elif(self.temp_time==0):
                    self.temp_time=temp_trasact_time
                    self.check_order_type(order=order)

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
                    temp_average=np.log(self.count_order_type_list[i][j]/col_list[j])
                    self.count_list.append(round(temp_average,4))
                else:
                    self.count_list.append(float(0))

    def remove_values(self):
        self.count_order_type_list = [[0 for _ in range(2)] for _ in range(4)]
        self.count_list = []
