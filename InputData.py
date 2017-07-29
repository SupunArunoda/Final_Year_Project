from pandas import DataFrame, read_csv, concat
from os import path
import numpy as np
from datetime import timedelta
from enum import Enum

class OrderEvent(Enum):
    SUBMISSION = 1
    CANCELLATION = 2
    DELETION = 3
    EXECUTION = 4
    HIDDEN_EXECUTION =5
    CROSS_TRADE = 6
    TRADING_HALT  = 7
    OTHER = 8

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

class LobsterData:
    def __init__(self):
        self.messages = DataFrame()
        self.processed_message= DataFrame();
        self.level = 0

    def read_single_day_data(self, message_file, append=True, convert_time=False):
        file_name = path.basename(message_file)
        file_base = path.splitext(file_name)[0]
        mydate = np.datetime64('{0}T00:00-0000'.format(file_base.split('_')[1]))

        mymessages = read_csv(message_file, header=None)

        mymessages.columns = ['Time', 'Event', 'Order_ID', 'Size', 'Price', 'Direction']
        mymessages.Event = mymessages['Event'].map(get_orderEvent)
        mymessages.Direction=mymessages['Direction'].map(get_orderDirection)
        #mymessages['Date'] = mydate

        #mymessages.set_index(['Order_ID'], inplace=True)

        self.messages = mymessages

    def get_type(self):
        return self.messages['Size'];

    def get_time_calculation(self):
        order_list=self.messages['Order_ID'];
        for i in order_list:
            x=i+1;
            for x in order_list:
                if(order_list.get_value(x)==order_list.get_value(i)):
                    self.messages['Event'].

        return order_list;
    def get_number_of_record(self):
        return self.messages;

