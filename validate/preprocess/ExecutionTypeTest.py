from orderbook.Order import Order
from orderbook.OrderBook import OrderBook
from pandas import read_csv
from preprocess.static.ExecutionType import ExecutionType

class ExecutionTypeTest:


    def run_execution_type(self,message_file,session_file,no_of_lines,time_delta):

        read_messages = read_csv(message_file, header=None)
        read_messages.columns = ['instrument_id', 'broker_id', 'executed_value', 'value', 'transact_time',
                                 'execution_type', 'order_qty', 'executed_qty', 'total_qty', 'side', 'visible_size',
                                 'order_id']
        data=read_messages

        exe_type=ExecutionType(session_file=session_file)

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

            writable_df = exe_type.get_time_frame(order=order,time_delta=time_delta)

            if index == no_of_lines and no_of_lines!=0:
                break
        print(writable_df)
        writable_df.to_csv("output/ex_type_log_based_time_framed.csv", index=False, encoding='utf-8')

