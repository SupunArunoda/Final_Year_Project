from pandas import DataFrame, read_csv
from datetime import datetime
from dateutil import parser as DUp
import numpy as np

from app.orderbook.Order import Order


class Entropy:
    def __init__(self):
        session_file = '../../data/sessions.csv'
        self.session = read_csv(session_file)
        self.regular_list = self.get_regular_time()
        print(self.regular_list)


    def get_regular_time(self):
        count = 0;
        reg_list = []
        for index, session_row in self.session.iterrows():
            session_name = session_row['session_name']
            if (session_name[:15] == 'Regular Trading'):
                reg_list.insert(count, DUp.parse(session_row['transact_time']))
                count += 1
        return reg_list

    def str_to_date_time(self, str_date_1, str_date_2):
        new_date_1 = datetime.strptime(str_date_1, '%Y-%m-%d %H:%M:%S.%f')
        new_date_2 = datetime.strptime(str_date_2, '%Y-%m-%d %H:%M:%S.%f')
        diff = ((new_date_2 - new_date_1).seconds) / 60
        return diff

    def get_valid_data(self, message_file):
        read_messages = read_csv(message_file, header=None)
        read_messages.columns = ['instrument_id', 'broker_id', 'executed_value', 'value', 'transact_time',
                                 'execution_type', 'order_qty', 'executed_qty', 'total_qty', 'side', 'visible_size',
                                 'order_id']
        data = read_messages
        temp = []
        for index, order_row in data.iterrows():
            order_id = order_row['order_id']
            visible_size = order_row['visible_size']
            side = order_row['side']
            total_qty = order_row['total_qty']
            executed_qty = order_row['executed_qty']
            order_qty = order_row['order_qty']
            execution_type = order_row['execution_type']
            transact_time = order_row['transact_time']
            value = order_row['value']
            executed_value = order_row['executed_value']
            broker_id = order_row['broker_id']
            instrument_id = order_row['instrument_id']  # set size attribute
            order = Order(order_id=order_id, visible_size=visible_size, side=side, total_qty=total_qty,
                          executed_qty=executed_qty
                          , order_qty=order_qty, execution_type=execution_type, transact_time=transact_time,
                          value=value, executed_value=executed_value
                          , broker_id=broker_id, instrument_id=instrument_id)

            temp_trasact_time = DUp.parse(order.transact_time)
            # temp_trasact_time = order.transact_time.to_datetime()

            for i in range(0, len(self.regular_list), 2):
                if (temp_trasact_time >= self.regular_list[i] and temp_trasact_time <= self.regular_list[i + 1]):
                    temp.append(temp_trasact_time)
        print(temp)

en = Entropy()
message_file = '../../data/data.csv'
en.get_valid_data(message_file = '../../data/data.csv')