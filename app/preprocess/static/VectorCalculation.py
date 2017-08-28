from pandas import DataFrame,read_csv
import datetime
import csv
import sys
from dateutil import parser as DUp

class VectorWindow:


    def __init__(self,session_file):

        self.messages = DataFrame()
        self.processed_message = DataFrame([]);

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
                        self.set_input(order=order)
                    else:
                        self.set_input(order=order)
                        self.get_calculation()
                        index=str(self.temp_time)+str('$$')+str(order.transact_time)
                        self.volume_average_list.append(index)
                        self.price_average_list.append(index)

                        self.temp_time=0
                    if(self.temp_time==0):
                        self.temp_time = temp_trasact_time

                elif(self.temp_time==0):
                    self.temp_time=temp_trasact_time

        return self.attributes;

    def set_input(self,order):
        self.messages = self.messages.append(DataFrame(
            {'Order_ID': order.order_id, 'Submitted_Time': order.transact_time, 'Size': order.visible_qty, 'Price': order.value,
             'Execution_Type' : order.execution_type,'Side': order.side}, index=[0]), ignore_index=True);


    def get_calculation(self):
        group=self.messages.groupby('Order_ID')['Submitted_Time'].unique()
        group=group[group.apply(lambda x: len(x)>1)]#remove orders not having at least two time values
        bestBid = 0
        bestAsk = sys.maxsize

        for index, order_row in group.iteritems():
            if(index>0):
                min=float(order_row[0])
                max=float(order_row[-1])
                diff=max-min#calculate the execution time for an order
                volume=self.messages.loc[self.messages['Order_ID'] == index, 'Size'].iloc[0]#set size attribute
                price = self.messages.loc[self.messages['Order_ID'] == index, 'Price'].iloc[0]  #set price attribute
                direction = self.messages.loc[self.messages['Order_ID'] == index, 'Side'].iloc[0]  #set direction attribute

        return self.processed_message;