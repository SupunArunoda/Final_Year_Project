from pandas import DataFrame,read_csv
import datetime
import csv
import numpy as np
from dateutil import parser as DUp




class PriceGapStatic:


    def     __init__(self,session_file,window):

        self.attributes = DataFrame()
        self.first_order=None;
        self.first_time = None;
        self.first_buy_order = None;
        self.first_sell_order = None;
        self.sell_attributes = DataFrame()
        self.buy_attributes = DataFrame()
        self.all_attributes=DataFrame()
        self.temp_time=0
        self.count=0

        self.first_broker=None;
        self.start_time=0
        self.anomaly_first_point=DUp.parse("2016-04-29 13:02:00")
        self.anomaly_second_point = DUp.parse("2016-04-29 13:22:00")

        self.session = session_file
        self.regular_list=self.get_regular_time()
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

    #get price gap from first
    def get_all_day_gap(self,order):
        if(self.first_order==None):
            self.first_order=order.value
        else:
            if(order.execution_type==15):
                price_gap = order.executed_value - self.first_order
                self.first_order = order.executed_value
            else:
                price_gap = order.value - self.first_order
                self.first_order = order.value
            self.attributes = self.attributes.append(DataFrame(
                {'time_index': order.transact_time,
                 'price_gap': price_gap
                 }, index=[0]), ignore_index=True);
        return self.attributes

    def get_regular_gap(self,order):
        for i in range(0, len(self.regular_list), 2):
            temp_trasact_time = DUp.parse(order.transact_time)
            if (temp_trasact_time >= self.regular_list[i] and temp_trasact_time <= self.regular_list[i + 1]):
                if (self.first_order==None):
                    if(order.execution_type==15):
                        self.first_order=order.executed_value
                    else:
                        self.first_order = order.value
                else:
                    if(order.execution_type==15):
                        price_gap = order.executed_value - self.first_order
                        self.first_order = order.executed_value
                    else:
                        price_gap = order.value - self.first_order
                        self.first_order = order.value
                    self.attributes = self.attributes.append(DataFrame({
                        'time_index': order.transact_time,
                        'price_gap': price_gap
                         }, index=[0]), ignore_index=True);

        return self.attributes

    def get_regular_gap_chunks(self, order,row_val):

        temp_trasact_time = DUp.parse(order.transact_time)
        for i in range(0, len(self.regular_list), 2):
            if (temp_trasact_time >= self.regular_list[i] and temp_trasact_time <= self.regular_list[i + 1]):
                if (self.window.isWindowLimitReach(order=order) == False):
                    self.get_calculation(order=order)
                    self.all_attributes = self.all_attributes.append(DataFrame(
                        {'order_id': order.order_id,
                         'visible_size': order.visible_size,
                         'side': order.side,
                         'total_qty': order.total_qty,
                         'executed_qty': order.executed_qty,
                         'order_qty': order.order_qty,
                         'execution_type': order.execution_type,
                         'transact_time': order.transact_time,
                         'value': order.value,
                         'executed_value': order.executed_value,
                         'broker_id': order.broker_id,
                         'instrument_id': order.instrument_id,
                         }, index=[0]), ignore_index=True);
                    if (self.temp_time == 0):
                        self.temp_time = temp_trasact_time
                else:
                    # self.get_calculation(order=order)
                    print(self.attributes)
                    self.get_calculation(order=order)
                    self.normalize_df()
                    self.count = self.count + 1
                    self.write_csv(count=self.count, row_val=row_val)
                    self.temp_time = 0
                    self.first_order = None;
                    self.attributes = DataFrame()
                    self.temp_time = temp_trasact_time

    def normalize_df(self):
        mean_price_gap=self.attributes['price_gap'].mean()
        std_price_gap=self.attributes['price_gap'].values.std(ddof=1)
        self.attributes['nom_price_gap']=(self.attributes['price_gap']-mean_price_gap)/std_price_gap

    def write_csv(self,count,row_val):
        self.attributes.to_csv("app/output/"+str(row_val)+"_price_gap_regular_"+str(count)+"_all.csv", index=False, encoding='utf-8')
        self.all_attributes.to_csv("app/output/" + str(row_val) + "_all_attributes_" + str(count) + ".csv",
                               index=False, encoding='utf-8')

    def  get_calculation(self,order):
        if(order.value>0):
            if (self.first_order==None):
                if(order.execution_type==15):
                    self.first_order=order.executed_value
                else:
                    self.first_order = order.value
                self.first_broker = order.broker_id
                self.start_time = order.transact_time
            else:
                if(order.execution_type==15):
                    price_gap = order.executed_value - self.first_order
                    self.first_order = order.executed_value
                else:
                    price_gap = order.value - self.first_order
                    self.first_order = order.value
                end_broker = order.broker_id
                start_broker = self.first_broker
                self.first_broker = order.broker_id
                self.attributes = self.attributes.append(DataFrame({
                'time_index': self.start_time+"$$"+order.transact_time,
                'price_gap': price_gap,
                    'start_broker':start_broker,
                    'end_broker':end_broker
                    }, index=[0]), ignore_index=True);
                self.start_time = order.transact_time

    def get_calculation_first(self, order):
        if (order.value > 0):
            if (self.first_order == None):
                if (order.execution_type == 15):
                    self.first_order = order.executed_value
            else:
                if (order.execution_type == 15):
                    price_gap = order.executed_value - self.first_order
                else:
                    price_gap = order.value - self.first_order
                self.attributes = self.attributes.append(DataFrame({
                    'time_index': order.transact_time,
                    'price_gap': price_gap
                }, index=[0]), ignore_index=True);

    def get_anomaly_area(self,order):

        temp_trasact_time = DUp.parse(order.transact_time)
        if (temp_trasact_time <= self.anomaly_second_point and temp_trasact_time >= self.anomaly_first_point):
            if (self.first_order==None):
                if (order.execution_type==15):
                    self.first_order = order.executed_value
                else:
                    self.first_order = order.value
            else:
                if (order.execution_type==15):
                    price_gap = order.executed_value - self.first_order
                    self.first_order = order.executed_value
                else:
                    price_gap = order.value - self.first_order
                    self.first_order = order.value
                self.attributes = self.attributes.append(DataFrame({
                    'time_index': order.transact_time,
                    'price_gap': price_gap
                        }, index=[0]), ignore_index=True);

        return self.attributes

    def get_get_anomaly_area_buy_sell_execute(self,order):
        temp_trasact_time = DUp.parse(order.transact_time)
        if (temp_trasact_time <= self.anomaly_second_point and temp_trasact_time >= self.anomaly_first_point):
            if (order.side == 1):  # filter non empty first buy order
                if(order.execution_type==15):
                    self.buy_attributes = self.buy_attributes.append(DataFrame({
                    'time_index': order.transact_time,
                    'buy_price_gap': order.executed_value
                }, index=[0]), ignore_index=True);

            elif (order.side == 2):  # filter non empty first sell order
                if (order.execution_type == 15):
                    self.sell_attributes = self.sell_attributes.append(DataFrame({
                    'time_index': order.transact_time,
                    'sell_price_gap': order.executed_value
                    }, index=[0]), ignore_index=True);

    def get_anomaly_area_buy_sell(self,order):

        temp_trasact_time = DUp.parse(order.transact_time)
        if (temp_trasact_time <= self.anomaly_second_point and temp_trasact_time >= self.anomaly_first_point):
            if (self.first_buy_order==None and order.side==1):#filter empty buy order
                if (order.execution_type==15):
                    self.first_buy_order = order.executed_value
                else:
                    self.first_buy_order = order.value
            elif(self.first_sell_order==None and order.side==2):
                if (order.execution_type==15):
                    self.first_sell_order = order.executed_value
                else:
                    self.first_sell_order = order.value
            elif(self.first_buy_order!=None and order.side==1):#filter non empty first buy order
                if (order.execution_type==15):
                    buy_price_gap = order.executed_value-self.first_buy_order
                    self.first_buy_order = order.executed_value
                else:
                    buy_price_gap = order.value-self.first_buy_order
                    self.first_buy_order = order.value
                self.buy_attributes = self.buy_attributes.append(DataFrame({
                    'time_index': order.transact_time,
                    'buy_price_gap': buy_price_gap
                }, index=[0]), ignore_index=True);

            elif (self.first_sell_order!=None and order.side==2):#filter non empty first sell order
                if (order.execution_type==15):
                    sell_price_gap = order.executed_value - self.first_sell_order
                    self.first_sell_order = order.executed_value
                else:
                    sell_price_gap = order.value - self.first_sell_order
                    self.first_sell_order = order.value
                self.sell_attributes = self.sell_attributes.append(DataFrame({
                    'time_index': order.transact_time,
                    'sell_price_gap': sell_price_gap
                }, index=[0]), ignore_index=True);

        #return self.anomaly_first_point

    def get_buy_data(self):
        return self.buy_attributes

    def get_sell_data(self):
        return self.sell_attributes

