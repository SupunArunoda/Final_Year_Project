from InputData import LobsterData
from orderbook.Order import Order
from orderbook.OrderBook import OrderBook
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
    message_file = './data/testdata_50.csv'
    lob=LobsterData()
    data=lob.read_single_day_data(message_file=message_file)

    orderBook=OrderBook(order_data=data)
    for index, order_row in data.iterrows():
        time = order_row['Time']
        type = order_row['Event']
        price = order_row['Price']
        direction = order_row['Direction']
        order_id= order_row['Order_ID']
        volume = order_row['Size']  # set size attribute
        order=Order(id=order_id,price=price,time=time,volume=volume,type=type,direction=direction)
        orderBook.processOrder(order=order)

    orderBook.printOrderBook()

order_book()
#test_read_single_date_files()
#analyze_model()