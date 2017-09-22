from pandas import DataFrame,read_csv
import datetime
import csv
import numpy as np
from dateutil import parser as DUp

from app.preprocess.Window.TimeWindow import TimeWindow


class OrderbookAttrStatic:


    def __init__(self,session_file):

        self.attributes = DataFrame()
        self.temp_time=0;
        self.volume_average_list = []
        self.detailsList=[0 for _ in range(5)]

        self.session = read_csv(session_file)
        self.regular_list=self.get_regular_time()
        # self.window = TimeWindow(no_of_events=no_of_events)


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

    def remove_values(self):
        self.volume_average_list = []
        self.detailsList = [0 for _ in range(5)]








