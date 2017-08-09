from InputData import InputData
from orderbook.Order import Order
from orderbook.OrderBook import OrderBook
#from spark.InputData import Spark
#from model.cluster.KMeans import Kmeans

def test_read_single_date_files():
    message_file = './data/data.csv'
    read=InputData()
    read.read_single_day_data(message_file=message_file)
    print(read.str_to_date_time(str_date_1="4/29/2016  12:11:01 AM",str_date_2="4/29/2016  3:55:00 PM"))

def analyze_model():
    message_file='./output/vecotrozed_AMZN_level_50_data.csv'
   # kml = Kmeans()
   # kml.read_vector_file(message_file=message_file)
#    kml.read_vector_file(message_file=message_file)

def order_book():
    message_file = './data/testdata_50.csv'
    lob=InputData()
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

#order_book()
test_read_single_date_files()
#analyze_model()