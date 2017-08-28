from pandas import DataFrame, read_csv
from os import path
import numpy as np
from enum import Enum
import sys
from datetime import datetime

"""
Name : OrderEvent 
Return : Map to Event
"""
class OrderEvent(Enum):
    SUBMISSION = 1
    CANCELLATION = 2
    DELETION = 3
    EXECUTION = 4
    HIDDEN_EXECUTION =5
    CROSS_TRADE = 6
    TRADING_HALT  = 7
    OTHER = 8

"""
Name : OrderDirection 
Return : Map to Order Direction
"""
class OrderDirection(Enum):
    SELLORDER=-1
    BUYORDER=1

__EventMap = {}

for e in OrderEvent:
    __EventMap[e.value] = e

def get_orderEvent(eventid):
    return __EventMap[eventid]

__DirectionMap = {}

for f in OrderDirection:
    __DirectionMap[f.value] = f

def get_orderDirection(eventid):
    return __DirectionMap[eventid]


"""
Name: LobsterData
Returns : Create time, volume & price vectors
"""
class InputData:

    """
    Name: Initiate method
    Returns : messages DataFrame, processed_message DataFrame
    """
    def __init__(self):
        self.messages = DataFrame()
        self.processed_message= DataFrame([]);

    """
    Name : Read single day data
    Reaturns : messages DataFrame('Time','Event','Order_ID','Size','Price','Direction')
    """
    def read_single_day_data(self, message_file):
        read_messages = read_csv(message_file, header=None)
        read_messages.columns = ['instrument_id', 'broker_id', 'executed_value','value','transact_time', 'execution_type', 'order_qty','executed_qty','total_qty','side','visible_size','order_id']
        #read_messages.Event = read_messages['Event'].map(get_orderEvent)
       # read_messages.Direction=read_messages['Direction'].map(get_orderDirection)
        self.messages = read_messages
        return self.messages

    """
    Name: str_to_date_time
    Returns : time difference in minutes
    """
    def str_to_date_time(self,str_date_1,str_date_2):
        new_date_1=datetime.strptime(str_date_1,'%Y-%m-%d %H:%M:%S.%f')
        new_date_2 = datetime.strptime(str_date_2, '%Y-%m-%d %H:%M:%S.%f')
        diff=((new_date_2-new_date_1).seconds)/60
        return diff


    """
    Name: get_calculation
    Returns : processed_messages DataFrame('Order_ID','Execution_Time','Volume','Price','Direction','Best_Bid_Ask')
    """
    @property
    def get_calculation(self):
        group=self.messages.groupby('order_id')['transact_time'].unique()
        group=group[group.apply(lambda x: len(x)>1)]#remove orders not having at least two time values
        bestBid = 0
        bestAsk = sys.maxsize

        for index, order_row in group.iteritems():

            min=order_row[0]
            max=order_row[-1]
            diff=self.str_to_date_time(str_date_1=min,str_date_2=max)#calculate the execution time for an order
            #diff=max-min#calculate the execution time for an order
            volume=self.messages.loc[self.messages['order_id'] == index, 'visible_size'].iloc[0]#set size attribute
            price = self.messages.loc[self.messages['order_id'] == index, 'value'].iloc[0]  #set price attribute
            direction = self.messages.loc[self.messages['order_id'] == index, 'side'].iloc[0]  #set direction attribute

            if (direction == 1):
                if (bestBid == 0):
                    self.processed_message = self.processed_message.append(DataFrame(
                        {'order_id': index, 'execution_time': diff, 'size': volume, 'value': price,
                            'direction': direction, 'best_bid_ask': price}, index=[0]), ignore_index=True);
                elif (bestBid > 0):
                    self.processed_message = self.processed_message.append(DataFrame(
                        {'order_id': index, 'execution_time': diff, 'size': volume, 'value': price,
                            'direction': direction, 'best_bid_ask': bestBid}, index=[0]), ignore_index=True)
                if (bestBid < price):
                    bestBid = price

            else:
                if (bestAsk == sys.maxsize):
                    self.processed_message = self.processed_message.append(DataFrame(
                        {'order_id': index, 'execution_time': diff, 'size': volume, 'price': price,
                            'direction': direction, 'best_bid_ask': price}, index=[0]), ignore_index=True);
                elif (bestBid > 0):
                    self.processed_message = self.processed_message.append(DataFrame(
                        {'order_id': index, 'execution_time': diff, 'size': volume, 'value': price,
                            'direction': direction, 'best_bid_ask': bestAsk}, index=[0]), ignore_index=True);
                if (bestAsk > price):
                    bestAsk = price
        return self.processed_message;

    """
    Name : Calculate the time vector
    Returns  : processed_message=DataFrame.append('time_vector')
    """
    def get_time_vector(self):
        self.processed_message['mult']=(self.processed_message.execution_time*self.processed_message.size);
        vol_sum=self.processed_message['size'].sum()
        mul_sum=self.processed_message['mult'].sum()
        weighted_avrge=mul_sum/vol_sum;
        self.processed_message['time_vector'] = (np.log(self.processed_message.execution_time/weighted_avrge));
        return self.processed_message;

    """
    Name  : Calculate the volume vector
    Returns  : processed_message = DataFrame.append('volume_vector')
    """
    def get_volume_vector(self):
        vol_sum = self.processed_message['size'].sum()
        vol_day=vol_sum/self.processed_message['order_id'].count();
        self.processed_message['volume_vector'] = (np.log(self.processed_message.size/vol_day));
        return self.processed_message;

    """
    Name  : Calculate the price vector
    Returns : processed_message = DataFrame.append('price_vector')
    """
    def get_price_vector(self):
        self.processed_message['price_vector'] = (np.log(self.processed_message.value/self.processed_message.best_bid_ask));
        return self.processed_message;

    """
    Name : Write DataFrame to csv
    Returns  : Processed csv file
    """
    def write_csv(self):
        self.processed_message.to_csv("output/vecotrozed_AMZN_level_50_data.csv", index=False, encoding='utf-8')

    def run_data_process(self,message_file):
        self.read_single_day_data(message_file=message_file)
        self.get_calculation()
        self.get_time_vector()
        self.get_volume_vector()
        print(self.get_price_vector())
        self.write_csv()