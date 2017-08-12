from InputData import InputData
from orderbook.Order import Order
from orderbook.OrderBook import OrderBook
from preprocess.Window import Window
from pandas import DataFrame,read_csv
import datetime
#from spark.InputData import Spark
#from model.cluster.KMeans import Kmeans

"""def test_read_single_date_files():
    message_file = './data/AAPL_2012-06-21_34200000_37800000_message_50.csv'

    lob = Spark()
    lob.read_data(message_file=message_file)"""
def analyze_model():
    message_file='./output/vecotrozed_AMZN_level_50_data.csv'
    kml = Kmeans()
    kml.read_vector_file(message_file=message_file)
#    kml.read_vector_file(message_file=message_file)

def order_book():
    message_file = './data/data.csv'
    session_file='./data/sessions.csv'
    lob=InputData()
    data=lob.read_single_day_data(message_file=message_file)

    orderBook=OrderBook(order_data=data,session_file=session_file)

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
        order=Order(order_id=order_id,visible_size=visible_size,side=side,total_qty=total_qty,executed_qty=executed_qty
                    ,order_qty=order_qty,execution_type=execution_type,transact_time=transact_time,value=value,executed_value=executed_value
                    ,broker_id=broker_id,instrument_id=instrument_id)
        writable_df=orderBook.processOrder(order=order)

        # if index==1000:
        #     break
    print(writable_df)
    writable_df.to_csv("output/time_framed_data.csv", index=False, encoding='utf-8')

    #orderBook.printOrderBook()
def window_test():
    session_file = './data/sessions.csv'
    window=Window(session_file=session_file)
    print(window.get_regular_time())


#print(datetime.timedelta(0,120))
order_book()
#test_read_single_date_files()
#analyze_model()
#window_test()