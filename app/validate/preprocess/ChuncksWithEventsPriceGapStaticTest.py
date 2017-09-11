from app.orderbook.Order import Order
from pandas import DataFrame, read_csv

from app.preprocess.WindowByEvents.PriceGapStaticByEvents import PriceGapStaticByEvents
from app.preprocess.static.PriceGapStatic import PriceGapStatic


class ChuncksWithEventsPriceGapStaticTest:

    def __init__(self):
        self.normalize_data_frame = DataFrame()
        self.buy_data=DataFrame()
        self.sell_data=DataFrame()

    def run_price_gap(self,message_file,session_file,no_of_lines):

        read_messages = read_csv(message_file, header=None)
        read_messages.columns = ['instrument_id', 'broker_id', 'executed_value', 'value', 'transact_time',
                                 'execution_type', 'order_qty', 'executed_qty', 'total_qty', 'side', 'visible_size',
                                 'order_id']
        data=read_messages
        print(len(data.index))
        pricegapstatic=PriceGapStaticByEvents(session_file=session_file)

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

            self.normalize_data_frame=pricegapstatic.get_regular_gap_chunks(order=order,no_of_events=1200)
            #self.normalize_data_frame=pricegapstatic.get_all_day_gap(order=order)
            #pricegapstatic.get_regular_gap_chunks(order=order,time_delta=1200)
            self.buy_data=pricegapstatic.get_buy_data()
            self.sell_data=pricegapstatic.get_sell_data()
            if index == no_of_lines and no_of_lines != 0:
                break

        self.normalize_buy_sell()
        #print(self.buy_data)
        #print(self.sell_data)
        #self.normalize_buy_sell()
        #self.normalize_data_frame.to_csv("output/price_gap_10_50_all.csv", index=False, encoding='utf-8')

        self.buy_data.to_csv("/app/output/price_gap_buy_anomaly.csv", index=False, encoding='utf-8')
        self.sell_data.to_csv("F:/Acadamic/Final Year Research/Project/Final_Year_Project/app/output/price_gap_sell_anomaly.csv", index=False, encoding='utf-8')

    def normalize_df(self):
        mean_price_gap=self.normalize_data_frame['price_gap'].mean()

        std_price_gap=self.normalize_data_frame['price_gap'].values.std(ddof=1)

        self.normalize_data_frame['nom_price_gap']=(self.normalize_data_frame['price_gap']-mean_price_gap)/std_price_gap

    def normalize_buy_sell(self):
        mean_buy_price_gap = self.buy_data['buy_price_gap'].mean()
        mean_sell_price_gap = self.sell_data['sell_price_gap'].mean()

        std_buy_price_gap = self.buy_data['buy_price_gap'].values.std(ddof=1)
        std_sell_price_gap = self.sell_data['sell_price_gap'].values.std(ddof=1)

        self.buy_data['nom_buy_price_gap'] = (self.buy_data['buy_price_gap'] - mean_buy_price_gap) / std_buy_price_gap
        self.sell_data['nom_sell_price_gap'] = (self.sell_data['sell_price_gap'] - mean_sell_price_gap) / std_sell_price_gap



