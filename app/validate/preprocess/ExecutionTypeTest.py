from app.db.PreprocessFile import PreprocessFile
# from app.db.PreprocessFileController import PreprocessFileController
from app.orderbook.Order import Order
from app.orderbook.OrderBook import OrderBook
from pandas import read_csv, DataFrame
from app.preprocess.static.ExecutionTypeStatic import ExecutionTypeStatic

from time import gmtime, strftime


class ExecutionTypeTest:
    def __init__(self):
        self.normalize_data_frame = DataFrame()

    def run_execution_type_static(self, message_file, session_file, no_of_lines, time_delta ,window):
        uploaded_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())

        output_path = "app/output/ex_type_static_normalize.csv"

        last_process_start = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        read_messages = read_csv(message_file)

        # read_messages.columns = ['instrument_id', 'broker_id', 'executed_value', 'value', 'transact_time',
        #                          'execution_type', 'order_qty', 'executed_qty', 'total_qty', 'side', 'visible_size',
        #                          'order_id']
        data = read_messages

        exe_type = ExecutionTypeStatic(session_file=session_file, window=window)

        return_data = {}
        return_data['new_orders_count'] = 0
        return_data['ammend_orders_count'] = 0
        return_data['cancel_orders_count'] = 0
        return_data['execute_orders_count'] = 0

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

            self.normalize_data_frame = exe_type.get_time_frame(order=order, time_delta=time_delta)

            if order_row['execution_type'] == 0:
                return_data['new_orders_count'] = return_data['new_orders_count'] + 1
            if order_row['execution_type'] == 4:
                return_data['cancel_orders_count'] = return_data['cancel_orders_count'] + 1
            if order_row['execution_type'] == 5:
                return_data['ammend_orders_count'] = return_data['ammend_orders_count'] + 1
            if order_row['execution_type'] == 15:
                return_data['execute_orders_count'] = return_data['execute_orders_count'] + 1

            if index == no_of_lines and no_of_lines != 0:
                break

        last_process_end = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        input_file = message_file
        output_file = output_path
        # pf = PreprocessFile(input_file=input_file, uploaded_time=uploaded_time, last_process_start=last_process_start,
        #                     last_process_end=last_process_end, output_file=output_file)
        # pfc = PreprocessFileController()
        # return_data['proprocess_index'] = pfc.saveProcessFile(pf)

        # print(self.normalize_data_frame)
        self.normalize_df(writable_df=self.normalize_data_frame)
        self.normalize_data_frame.to_csv(output_path, index=False, encoding='utf-8')

        return_data['total_rows'] = len(data)
        return return_data

    def normalize_df(self, writable_df):
        mean_buy_execute = self.normalize_data_frame['execute_order_buy_average'].mean()
        mean_sell_execute = self.normalize_data_frame['execute_order_sell_average'].mean()
        mean_buy_new = self.normalize_data_frame['new_order_buy_average'].mean()
        mean_sell_new = self.normalize_data_frame['new_order_sell_average'].mean()
        mean_buy_ammend = self.normalize_data_frame['ammend_order_buy_average'].mean()
        mean_sell_ammend = self.normalize_data_frame['ammend_order_sell_average'].mean()
        mean_buy_cancel = self.normalize_data_frame['cancel_order_buy_average'].mean()
        mean_sell_cancel = self.normalize_data_frame['cancel_order_sell_average'].mean()

        mean_execute = self.normalize_data_frame['execute_order_average'].mean()
        mean_new = self.normalize_data_frame['new_order_average'].mean()
        mean_cancel = self.normalize_data_frame['cancel_order_average'].mean()
        mean_ammend = self.normalize_data_frame['ammend_order_average'].mean()

        std_buy_execute = self.normalize_data_frame['execute_order_buy_average'].values.std(ddof=1)
        std_sell_execute = self.normalize_data_frame['execute_order_sell_average'].values.std(ddof=1)
        std_buy_new = self.normalize_data_frame['new_order_buy_average'].values.std(ddof=1)
        std_sell_new = self.normalize_data_frame['new_order_sell_average'].values.std(ddof=1)
        std_buy_ammend = self.normalize_data_frame['ammend_order_buy_average'].values.std(ddof=1)
        std_sell_ammend = self.normalize_data_frame['ammend_order_sell_average'].values.std(ddof=1)
        std_buy_cancel = self.normalize_data_frame['cancel_order_buy_average'].values.std(ddof=1)
        std_sell_cancel = self.normalize_data_frame['cancel_order_sell_average'].values.std(ddof=1)

        std_execute = self.normalize_data_frame['execute_order_average'].values.std(ddof=1)
        std_new = self.normalize_data_frame['new_order_average'].values.std(ddof=1)
        std_cancel = self.normalize_data_frame['cancel_order_average'].values.std(ddof=1)
        std_ammend = self.normalize_data_frame['ammend_order_average'].values.std(ddof=1)

        print(mean_buy_execute, std_buy_execute, mean_sell_ammend, std_sell_ammend)

        self.normalize_data_frame['nom_exe_buy'] = (self.normalize_data_frame[
                                                        'execute_order_buy_average'] - mean_buy_execute) / std_buy_execute
        self.normalize_data_frame['nom_exe_sell'] = (self.normalize_data_frame[
                                                         'execute_order_sell_average'] - mean_sell_execute) / std_sell_execute
        self.normalize_data_frame['nom_new_buy'] = (self.normalize_data_frame[
                                                        'new_order_buy_average'] - mean_buy_new) / std_buy_new
        self.normalize_data_frame['nom_new_sell'] = (self.normalize_data_frame[
                                                         'new_order_sell_average'] - mean_sell_new) / std_sell_new

        self.normalize_data_frame['nom_amm_buy'] = (self.normalize_data_frame[
                                                        'ammend_order_buy_average'] - mean_buy_ammend) / std_buy_ammend
        self.normalize_data_frame['nom_amm_sell'] = (self.normalize_data_frame[
                                                         'ammend_order_sell_average'] - mean_sell_ammend) / std_sell_ammend
        self.normalize_data_frame['nom_can_buy'] = (self.normalize_data_frame[
                                                        'cancel_order_buy_average'] - mean_buy_cancel) / std_buy_cancel
        self.normalize_data_frame['nom_can_sell'] = (self.normalize_data_frame[
                                                         'cancel_order_sell_average'] - mean_sell_cancel) / std_sell_cancel

        self.normalize_data_frame['nom_exe'] = (self.normalize_data_frame[
                                                    'execute_order_average'] - mean_execute) / std_execute
        self.normalize_data_frame['nom_new'] = (self.normalize_data_frame['new_order_average'] - mean_new) / std_new
        self.normalize_data_frame['nom_can'] = (self.normalize_data_frame[
                                                    'cancel_order_average'] - mean_cancel) / std_cancel
        self.normalize_data_frame['nom_amm'] = (self.normalize_data_frame[
                                                    'ammend_order_average'] - mean_ammend) / std_ammend
