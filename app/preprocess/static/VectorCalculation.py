from pandas import DataFrame,read_csv
import datetime
import csv
from dateutil import parser as DUp

class VectorWindow:


    def __init__(self,session_file):

        self.attributes = DataFrame()
        self.temp_time=0;

        self.order_price_list = [[0 for _ in range(2)] for _ in range(3)]
        self.price_average_list = []
        self.count_order_list = [[0 for _ in range(2)] for _ in range(3)]

        self.order_volume_list = [[0 for _ in range(2)] for _ in range(3)]
        self.volume_average_list = []
        self.count_order_volume_list = [[0 for _ in range(2)] for _ in range(3)]

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

    def get_time_frame(self,order,time_delta):
        const_time_gap=datetime.timedelta(0, time_delta)#set time window value
        temp_trasact_time=DUp.parse(order.transact_time)
        for i in range(0,len(self.regular_list),2):
            if(temp_trasact_time>=self.regular_list[i] and temp_trasact_time<=self.regular_list[i+1]):
                if(self.temp_time!=0):
                    time_gap=temp_trasact_time-self.temp_time;
                    if(time_gap<=const_time_gap):
                        self.check_order(order=order)
                    else:
                        self.check_order(order=order)

                        index=str(self.temp_time)+str('$$')+str(order.transact_time)
                        self.volume_average_list.append(index)
                        self.price_average_list.append(index)
                        self.get_average_volume()
                        self.get_average_price()
                        self.attributes = self.attributes.append(DataFrame(
                            {'time_index_volume': self.volume_average_list[0],
                             'new_order_buy_volume': self.volume_average_list[1],
                             'new_order_sell_volume': self.volume_average_list[2],
                             'cancel_order_buy_volume': self.volume_average_list[3],
                             'cancel_order_sell_volume': self.volume_average_list[4],
                             'execute_order_buy_volume': self.volume_average_list[5],
                             'execute_order_sell_volume': self.volume_average_list[6],

                             'new_order_buy_price': self.price_average_list[1],
                             'new_order_sell_price': self.price_average_list[2],
                             'cancel_order_buy_price': self.price_average_list[3],
                             'cancel_order_sell_price': self.price_average_list[4],
                             'execute_order_buy_price': self.price_average_list[5],
                             'execute_order_sell_price': self.price_average_list[6]
                             }, index=[0]), ignore_index=True);

                        self.remove_values()
                        self.temp_time=0
                    if(self.temp_time==0):
                        self.temp_time = temp_trasact_time

                elif(self.temp_time==0):
                    self.temp_time=temp_trasact_time
                    self.check_order(order=order)

        return self.attributes;
