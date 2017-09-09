from pandas import DataFrame,read_csv
import datetime
import csv
import numpy as np
from dateutil import parser as DUp

class OrderbookAttrStatic:


    def __init__(self,session_file):

        self.attributes = DataFrame()
        self.temp_time=0;

        # self.order_price_list = [[0 for _ in range(2)] for _ in range(3)]
        # self.price_average_list = []
        # self.count_order_list = [[0 for _ in range(2)] for _ in range(3)]
        #
        # self.order_volume_list = [[0 for _ in range(2)] for _ in range(3)]
        self.volume_average_list = []
        # self.count_order_volume_list = [[0 for _ in range(2)] for _ in range(3)]
        self.detailsList=[0 for _ in range(5)]

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

    def get_time_frame(self,order,time_delta, details):
        const_time_gap=datetime.timedelta(0, time_delta)#set time window value
        temp_trasact_time=DUp.parse(order.transact_time)
        for i in range(0,len(self.regular_list),2):
            if(temp_trasact_time>=self.regular_list[i] and temp_trasact_time<=self.regular_list[i+1]):
                if(self.temp_time!=0):
                    time_gap=temp_trasact_time-self.temp_time;
                    if(time_gap<=const_time_gap):
                        self.check_order(order=order,details=details)
                    else:
                        self.check_order(order=order,details=details)

                        index=str(self.temp_time)+str('$$')+str(order.transact_time)
                        self.volume_average_list.append(index)
                        self.attributes = self.attributes.append(DataFrame(
                            {'time_index': self.volume_average_list[0],
                             'best_bid_avg': self.detailsList[0]/self.detailsList[4],
                             'best_ask_avg': self.detailsList[1]/self.detailsList[4],
                             'top_buy_vol_avg': self.detailsList[2]/self.detailsList[4],
                             'top_sell_vol_avg': self.detailsList[3]/self.detailsList[4]
                             }, index=[0]), ignore_index=True);

                        self.remove_values()
                        self.temp_time=0
                    if(self.temp_time==0):
                        self.temp_time = temp_trasact_time

                elif(self.temp_time==0):
                    self.temp_time=temp_trasact_time
                    self.check_order(order=order, details=details)

        return self.attributes;

    def check_order(self,order,details):
        self.detailsList[0] += details[0]
        self.detailsList[1] += details[1]
        self.detailsList[2] += details[2]
        self.detailsList[3] += details[3]
        self.detailsList[4] += 1

    # def count_order_price(self,order,type):
    #     if (order.side == 1):#buy order check
    #         self.order_price_list[type][0]+=order.value
    #         self.count_order_list[type][0]+=1
    #
    #     elif (order.side == 2):#sell order check
    #         self.order_price_list[type][1] += order.value
    #         self.count_order_list[type][1] += 1
    #
    # def count_order_volume(self, order, type):
    #     if order.side == 1:  # buy order check
    #         if type == 2:
    #             self.order_volume_list[type][0] += order.executed_qty
    #             self.count_order_volume_list[type][0] += 1
    #         else:
    #             self.order_volume_list[type][0] += order.visible_size
    #             self.count_order_volume_list[type][0] += 1
    #
    #     elif order.side == 2:  # sell order check
    #         if type == 2:
    #             self.order_volume_list[type][1] += order.executed_qty
    #             self.count_order_volume_list[type][1] += 1
    #         else:
    #             self.order_volume_list[type][1] += order.visible_size
    #             self.count_order_volume_list[type][1] += 1
    #
    # def get_average_price(self):
    #
    #     for i in range(len(self.order_price_list)):
    #         for j in range(len(self.order_price_list[i])):
    #             if(self.count_order_list[i][j]!=0):
    #                 temp_average=(self.order_price_list[i][j]/self.count_order_list[i][j])
    #                 self.price_average_list.append(round(temp_average,4))
    #                 #self.price_average_list.append(self.count_order_list[i][j])
    #             else:
    #                 self.price_average_list.append(float(0))
    #
    #
    # def get_average_volume(self):
    #
    #     for i in range(len(self.order_volume_list)):
    #         for j in range(len(self.order_volume_list[i])):
    #             if(self.count_order_volume_list[i][j]!=0):
    #                 temp_average=(self.order_volume_list[i][j]/self.count_order_volume_list[i][j])
    #                 self.volume_average_list.append(round(temp_average,4))
    #                 #self.volume_average_list.append(self.count_order_list[i][j])
    #             else:
    #                 self.volume_average_list.append(float(0))


    def remove_values(self):
        # self.order_volume_list = [[0 for _ in range(2)] for _ in range(3)]
        self.volume_average_list = []
        # self.count_order_volume_list = [[0 for _ in range(2)] for _ in range(3)]
        #
        # self.order_price_list = [[0 for _ in range(2)] for _ in range(3)]
        # self.price_average_list = []
        # self.count_order_list = [[0 for _ in range(2)] for _ in range(3)]
        self.detailsList = [0 for _ in range(5)]








