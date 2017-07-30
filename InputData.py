from pandas import DataFrame, read_csv, concat
from os import path
import numpy as np
from enum import Enum
import sys

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
class LobsterData:

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
        read_messages.columns = ['Time', 'Event', 'Order_ID', 'Size', 'Price', 'Direction']
        read_messages.Event = read_messages['Event'].map(get_orderEvent)
        read_messages.Direction=read_messages['Direction'].map(get_orderDirection)
        self.messages = read_messages

    """
    Name: get_calculation
    Returns : processed_messages DataFrame('Order_ID','Execution_Time','Volume','Price','Direction','Best_Bid_Ask')
    """
    @property
    def get_calculation(self):
        group=self.messages.groupby('Order_ID')['Time'].unique()
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
                direction = self.messages.loc[self.messages['Order_ID'] == index, 'Direction'].iloc[0]  #set direction attribute

                if (direction == OrderDirection.BUYORDER):
                    if (bestBid == 0):
                        self.processed_message = self.processed_message.append(DataFrame(
                            {'Order_ID': index, 'Execution_Time': diff, 'Volume': volume, 'Price': price,
                             'Direction': direction, 'Best_Bid_Ask': price}, index=[0]), ignore_index=True);
                    elif (bestBid > 0):
                        self.processed_message = self.processed_message.append(DataFrame(
                            {'Order_ID': index, 'Execution_Time': diff, 'Volume': volume, 'Price': price,
                             'Direction': direction, 'Best_Bid_Ask': bestBid}, index=[0]), ignore_index=True)
                    if (bestBid < price):
                        bestBid = price

                else:
                    if (bestAsk == sys.maxsize):
                        self.processed_message = self.processed_message.append(DataFrame(
                            {'Order_ID': index, 'Execution_Time': diff, 'Volume': volume, 'Price': price,
                             'Direction': direction, 'Best_Bid_Ask': price}, index=[0]), ignore_index=True);
                    elif (bestBid > 0):
                        self.processed_message = self.processed_message.append(DataFrame(
                            {'Order_ID': index, 'Execution_Time': diff, 'Volume': volume, 'Price': price,
                             'Direction': direction, 'Best_Bid_Ask': bestAsk}, index=[0]), ignore_index=True);
                    if (bestAsk > price):
                        bestAsk = price
        return self.processed_message;

    """
    Name : Calculate the time vector
    Returns  : processed_message=DataFrame.append('time_vector')
    """
    def get_time_vector(self):
        self.processed_message['mult']=(self.processed_message.Execution_Time*self.processed_message.Volume);
        vol_sum=self.processed_message['Volume'].sum()
        mul_sum=self.processed_message['mult'].sum()
        weighted_avrge=mul_sum/vol_sum;
        self.processed_message['time_vector'] = (np.log(self.processed_message.Execution_Time/weighted_avrge));
        return self.processed_message;

    """
    Name  : Calculate the volume vector
    Returns  : processed_message = DataFrame.append('volume_vector')
    """
    def get_volume_vector(self):
        vol_sum = self.processed_message['Volume'].sum()
        vol_day=vol_sum/self.processed_message['Order_ID'].count();
        self.processed_message['volume_vector'] = (np.log(self.processed_message.Volume/vol_day));
        return self.processed_message;

    """
    Name  : Calculate the price vector
    Returns : processed_message = DataFrame.append('price_vector')
    """
    def get_price_vector(self):
        self.processed_message['price_vector'] = (np.log(self.processed_message.Price/self.processed_message.Best_Bid_Ask));
        return self.processed_message;

    """
    Name : Write DataFrame to csv
    Returns  : Processed csv file
    """
    def write_csv(self):
        self.processed_message.to_csv("output/vecotrozed_AMZN_level_50_data.csv", index=False, encoding='utf-8')

    def run_data_process(self,message_file):
        self.read_single_day_data(message_file=message_file)
        self.get_calculation
        self.get_time_vector()
        self.get_volume_vector()
        print(self.get_price_vector())
        self.write_csv()