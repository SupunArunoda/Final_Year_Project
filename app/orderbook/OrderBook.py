from pandas import DataFrame

from preprocess.static.OrderbookAttrStatic import OrderbookAttrStatic
from app.preprocess.static.PriceVolumeAverage import Window


class OrderBook:
    buyOrders = []
    sellOrders = []

    buyOrdersDetails = {}
    sellOrdersDetails = {}
    indx=0

    def __init__(self, order_data,session_file):
        self.order_d = order_data
        columns = ['instrument_id', 'broker_id', 'executed_value', 'value', 'transact_time', 'execution_type',
                   'order_qty', 'executed_qty', 'total_qty', 'side', 'visible_size', 'order_id']
        self.neworders = DataFrame(columns=columns)
        self.window=OrderbookAttrStatic(session_file=session_file)


    """
        Name : Process Order
        Process the order as its 4 types
        0-> New Order
        4-> Cancel Order
        5-> Amend Order
        15-> Fill Order
     """
    def processOrder(self, order,time_delta):
        self.indx += 1
        if(order.value>0):

            # if len(self.buyOrders)>0 and len(self.sellOrders)>0 and self.indx>500:
            #     if self.buyOrders[0] > self.sellOrders[0]:
            #         print("new")
            #time function here

            if order.execution_type == 0:
                self.addNewOrder(order)
            elif order.execution_type == 4:
                self.cancelOrder(order)
            elif order.execution_type == 5:
                self.amendOrder(order)
            elif order.execution_type == 15:
                self.fillOrder(order)
            # detail=self.getDetails()
            # df = self.window.get_time_frame(order=order, time_delta=time_delta, details=detail)
            # return df

    """
            Name : Add new order
            This is to add new order (type 0) to order book
    """
    def addNewOrder(self, order):
        #to keep track of total volume of a order
        tempDataFrame=self.neworders[(self.neworders['order_id'] == order.order_id) & (self.neworders['execution_type'] == 0)]
        if(tempDataFrame.count().iloc[0]==0):
            self.neworders = self.neworders.append(self.order_d[(self.order_d['order_id'] == order.order_id) & (self.order_d['execution_type'] == 0)], ignore_index=True);
        # elif(tempDataFrame.count().iloc[0]>0):
        #     self.neworders.loc[((self.neworders['order_id'] == order.order_id) & (self.neworders['execution_type'] == 0)), 'visible_size'] += order.visible_size

         #to check buy sell orders seperately
        if order.side == 1:
            self.addNewBuyOrder(order)
        else:
            self.addNewSellOrder(order)

    def addNewBuyOrder(self, order):
        if order.value not in self.buyOrders:
            self.buyOrders.append(order.value)
            self.buyOrders.sort(reverse=True)
            self.buyOrdersDetails[order.value] = [order.order_id]
        else:
            self.buyOrdersDetails[order.value].append(order.order_id)

    def addNewSellOrder(self, order):
        if order.value not in self.sellOrders:
            self.sellOrders.append(order.value)
            self.sellOrders.sort()
            self.sellOrdersDetails[order.value] = [order.order_id]
        else:
            self.sellOrdersDetails[order.value].append(order.order_id)

    """
                Name : Cancel Order
                This is to cancel order (type 4) of order book
                first remove the corresponding order id from the list
                then if the list of that price point is empty then remove the price point also
    """
    def cancelOrder(self, order):
        if order.side == 1:  # buy order cancellation
            tempList = []
            if order.value in self.buyOrdersDetails.keys():
                tempList = self.buyOrdersDetails[order.value]

                for tempOrderId in tempList:
                    if order.order_id == tempOrderId:
                        self.buyOrdersDetails[order.value].remove(tempOrderId)
                        break
                if len(tempList) == 0:
                    del self.buyOrdersDetails[order.value]
                    self.buyOrders.remove(order.value)

        else:  # sell order cancellation
            tempList = []
            if order.value in self.sellOrdersDetails.keys():
                tempList = self.sellOrdersDetails[order.value]

                for tempOrderId in tempList:
                    if order.order_id == tempOrderId:
                        self.sellOrdersDetails[order.value].remove(tempOrderId)
                        break

                if len(tempList) == 0:
                    del self.sellOrdersDetails[order.value]
                    self.sellOrders.remove(order.value)

    """
                Name : Fill order
                This is to deal with fill (type 15) orders
                Fill orders -> orders that has been matched
                First reduce the executed volume of the corresponding order
                If its executed with the total visible qty then do the same thing as cancel order
    """
    def fillOrder(self, order):
        if order.side == 1:  # if buy order
            price=self.neworders.loc[((self.neworders['order_id'] == order.order_id) & (self.neworders['execution_type'] == 0)),'value']
            if price.empty==False:
                # tempOrder = self.neworders[(self.neworders['order_id'] == order.order_id) & (self.neworders['execution_type'] == 0)]
                # volume = tempOrder['visible_size'].iloc[0]
                # diff = (volume - order.executed_qty)
                self.neworders.loc[((self.neworders['order_id'] == order.order_id) & (self.neworders['execution_type'] == 0)), 'visible_size'] = order.visible_size

                if order.total_qty == 0:
                    self.cancelOrder(order=order)

        else:  # if sell order
            price = self.neworders.loc[
                ((self.neworders['order_id'] == order.order_id) & (self.neworders['execution_type'] == 0)), 'value']
            if price.empty==False:
                # tempOrder = self.neworders[(self.neworders['order_id'] == order.order_id) & (self.neworders['execution_type'] == 0)]
                # volume = tempOrder['visible_size'].iloc[0]
                # diff = (volume - order.executed_qty)
                self.neworders.loc[((self.neworders['order_id'] == order.order_id) & (self.neworders['execution_type'] == 0)), 'visible_size'] = order.visible_size

                if order.total_qty == 0:
                    self.cancelOrder(order=order)

    """
                Name : Amend Order
                This is to change details of amend (type 5) orders
                First replace the corresponding entry of the database
                then to change the values cancel the previous order and add new order with new values
    """
    def amendOrder(self, order):
        price=0
        price = self.neworders.loc[
            ((self.neworders['order_id'] == order.order_id) & (self.neworders['execution_type'] == 0)), 'value']
        if price.empty == False:
            type=0
            self.neworders.loc[
                ((self.neworders['order_id'] == order.order_id) & (
                self.neworders['execution_type'] == 0))] = [order.instrument_id, order.broker_id, order.executed_value, order.value, order.transact_time, type ,
                                                            order.order_qty, order.executed_qty, order.total_qty, order.side, order.visible_size, order.order_id]

            if price.iloc[0] != order.value:
                if order.side==1:
                    if price.iloc[0] in self.buyOrdersDetails.keys():
                        tempList = self.buyOrdersDetails[price.iloc[0]]

                        for tempOrderId in tempList:
                            if order.order_id == tempOrderId:
                                self.buyOrdersDetails[price.iloc[0]].remove(tempOrderId)
                                break
                        if len(tempList) == 0:
                            del self.buyOrdersDetails[price.iloc[0]]
                            self.buyOrders.remove(price.iloc[0])
                    self.addNewBuyOrder(order=order)
                else:
                    if price.iloc[0] in self.sellOrdersDetails.keys():
                        tempList = self.sellOrdersDetails[price.iloc[0]]

                        for tempOrderId in tempList:
                            if order.order_id == tempOrderId:
                                self.sellOrdersDetails[price.iloc[0]].remove(tempOrderId)
                                break

                        if len(tempList) == 0:
                            del self.sellOrdersDetails[price.iloc[0]]
                            self.sellOrders.remove(price.iloc[0])
                    self.addNewSellOrder(order=order)
            #print (order.value)

    def printOrderBook(self):
        print("Count\t\tVolume\t\t\t@ Price")
        for buyOrder in self.buyOrders:
            volume = 0
            for orderId in self.buyOrdersDetails[buyOrder]:
                order = self.neworders.loc[(self.neworders['order_id'] == orderId) & (self.neworders['execution_type'] == 0)]
                if order.empty==False:
                    volume += order['visible_size'].iloc[0]

            print(len(self.buyOrdersDetails[buyOrder]), "\t\t\t", volume, "\t\t\t @", buyOrder)

        print("\n\n\n")
        print("Count\t\tVolume\t\t\t@ Price")
        for sellOrder in self.sellOrders:
            volume = 0
            for orderId in self.sellOrdersDetails[sellOrder]:
                order = self.neworders.loc[(self.neworders['order_id'] == orderId) & (self.neworders['execution_type'] == 0)]
                if order.empty==False:
                    volume += order['visible_size'].iloc[0]

            print(len(self.sellOrdersDetails[sellOrder]), "\t\t\t", volume, "\t\t\t @", sellOrder)


    def getDetails(self):
        details=[]
        if(len(self.buyOrders)>0):
            details.append(self.buyOrders[0])
        else:
            details.append(0)

        if (len(self.sellOrders) > 0):
            details.append(self.sellOrders[0])
        else:
            details.append(0)
        volume = 0
        count=0
        for buyOrder in self.buyOrders:
            count+=1
            if(count>10):
                break
            for orderId in self.buyOrdersDetails[buyOrder]:
                order = self.neworders.loc[(self.neworders['order_id'] == orderId) & (self.neworders['execution_type'] == 0)]
                if order.empty==False:
                    volume += order['visible_size'].iloc[0]

        details.append(volume/10)

        volume = 0
        count = 0
        for sellOrder in self.sellOrders:
            count += 1
            if (count > 10):
                break
            for orderId in self.sellOrdersDetails[sellOrder]:
                order = self.neworders.loc[(self.neworders['order_id'] == orderId) & (self.neworders['execution_type'] == 0)]
                if order.empty==False:
                    volume += order['visible_size'].iloc[0]

        details.append(volume / 10)

        return details