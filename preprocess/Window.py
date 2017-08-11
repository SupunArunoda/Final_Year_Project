from pandas import DataFrame,read_csv
import datetime
import csv
from dateutil import parser as DUp

class Window:


    def __init__(self,session_file):

        self.attributes = DataFrame()
        self.temp_time=0;
        self.order_price_list = [[0 for _ in range(2)] for _ in range(3)]
        self.price_average_list = []
        self.count_order_list = [[0 for _ in range(2)] for _ in range(3)]

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

    def get_time_frame(self,order):
        const_time_gap=datetime.timedelta(0, 240)#set time window value
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
                        self.price_average_list.append(index)
                        self.get_average()
                        self.attributes = self.attributes.append(DataFrame(
                            {'time_index': self.price_average_list[0], 'new_order_buy': self.price_average_list[1], 'new_order_sell': self.price_average_list[2], 'cancel_order_buy': self.price_average_list[3],
                             'cancel_order_sell': self.price_average_list[4], 'execute_order_buy': self.price_average_list[5], 'execute_order_sell': self.price_average_list[6]}, index=[0]), ignore_index=True);

                        self.remove_values()
                        self.temp_time=0
                    if(self.temp_time==0):
                        self.temp_time = temp_trasact_time

                elif(self.temp_time==0):
                    self.temp_time=temp_trasact_time
                    self.check_order(order=order)

        return self.attributes;

    def check_order(self,order):
        if order.execution_type==0:#new order check
            self.count_order(order=order,type=0)
        elif order.execution_type==4:#cancel order check
            self.count_order(order=order,type=1)
        elif order.execution_type == 15:#execution order
            self.count_order(order=order, type=2)


    def count_order(self,order,type):
        if (order.side == 1):#buy order check
            self.order_price_list[type][0]+=order.value
            self.count_order_list[type][0]+=1

        elif (order.side == 2):#sell order check
            self.order_price_list[type][1] += order.value
            self.count_order_list[type][1] += 1

    def get_average(self):

        for i in range(len(self.order_price_list)):
            for j in range(len(self.order_price_list[i])):
                if(self.count_order_list[i][j]!=0):
                    temp_average=self.order_price_list[i][j]/self.count_order_list[i][j]
                    self.price_average_list.append(round(temp_average,4))

                else:
                    self.price_average_list.append(float(0))



    def remove_values(self):
        self.order_price_list = [[0 for _ in range(2)] for _ in range(3)]
        self.price_average_list = []
        self.count_order_list = [[0 for _ in range(2)] for _ in range(3)]








