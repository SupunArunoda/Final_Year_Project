from app.orderbook.Order import Order
from app.orderbook.OrderBook import OrderBook
from pandas import read_csv

from app.preprocess.static.OrderbookSimulation import OrderbookSimulation
from pandas import DataFrame,read_csv
import numpy as np

class OrderbookSimulationTest:

    def __init__(self):
        self.df = DataFrame()

    def run_orderbook_simulation(self,message_file,session_file, window):

        read_messages = read_csv(message_file)
        # read_messages.columns = ['instrument_id', 'broker_id', 'executed_value', 'value', 'transact_time',
        #                          'execution_type', 'order_qty', 'executed_qty', 'total_qty', 'side', 'visible_size',
        #                          'order_id']

        simulation=OrderbookSimulation(session_file=session_file,data_file=read_messages ,window=window)
        data=read_messages

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

            simulation.get_time_frame(order=order)
            # if index > no_of_lines:
            #     break

        # print(df)
        # self.df.to_csv("F:/Hishara/FYP/Final_Year_Project/app/output/orderbook_simulation.csv", index=False,encoding='utf-8')


