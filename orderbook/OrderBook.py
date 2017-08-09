from pandas import DataFrame


class OrderBook:
    buyOrders = []
    sellOrders = []

    buyOrdersDetails = {}
    sellOrdersDetails = {}

    def __init__(self, order_data):
        self.order_d = order_data

    def processOrder(self, order):
        if order.type == 1:
            self.addNewOrder(order)
        elif order.type == 3:
            self.cancelOrder(order)
        elif order.type == 4 or order.type == 5:
            self.executeOrder(order)

    def addNewOrder(self, order):
        if order.direction == 1:
            self.addNewBuyOrder(order)
        else:
            self.addNewSellOrder(order)

    def addNewBuyOrder(self, order):
        if order.price not in self.buyOrders:
            self.buyOrders.append(order.price)
            self.buyOrders.sort(reverse=True)
            self.buyOrdersDetails[order.price] = [order.id]
        else:
            self.buyOrdersDetails[order.price].append(order.id)

    def addNewSellOrder(self, order):
        if order.price not in self.sellOrders:
            self.sellOrders.append(order.price)
            self.sellOrders.sort()
            self.sellOrdersDetails[order.price] = [order.id]
        else:
            self.sellOrdersDetails[order.price].append(order.id)

    def cancelOrder(self, order):
        if order.direction == 1:  # buy order cancellation
            tempList = []
            if order.price in self.sellOrdersDetails.keys():
                tempList = self.sellOrdersDetails[order.price]

                for tempOrderId in tempList:
                    if order.id == tempOrderId:
                        self.buyOrdersDetails[order.price].remove(tempOrderId)
                        break
                if len(tempList) == 0:
                    del self.buyOrdersDetails[order.price]
                    self.buyOrders.remove(order.price)

        else:  # sell order cancellation
            tempList = []
            if order.price in self.sellOrdersDetails.keys():
                tempList = self.sellOrdersDetails[order.price]

                for tempOrderId in tempList:
                    if order.id == tempOrderId:
                        self.sellOrdersDetails[order.price].remove(tempOrderId)
                        break

                if len(tempList) == 0:
                    del self.sellOrdersDetails[order.price]
                    self.sellOrders.remove(order.price)

    def executeOrder(self, order):
        if order.direction == 1:  # if buy order
            if order.price in self.buyOrdersDetails.keys():
                tempOrder = self.order_d[self.order_d['Order_ID'] == order.id and self.order_d['Event'] == 1]
                volume = tempOrder['Size']
                diff = volume - order.size
                self.order_d[self.order_d['Order_ID'] == order.id and self.order_d['Event'] == 1]['Size'] = diff

                if diff == 0:
                    self.cancelOrder(order=order)

        else:  # if sell order
            if order.price in self.sellOrdersDetails.keys():
                if order.price in self.sellOrdersDetails.keys():
                    tempOrder = self.order_d[(self.order_d['Order_ID'] == order.id) & (self.order_d['Event'] == 1)]
                    volume = tempOrder['Size']
                    diff = volume - order.volume
                    self.order_d[(self.order_d['Order_ID'] == order.id) & (self.order_d['Event'] == 1)]['Size'] = diff

                    if diff == 0:
                        self.cancelOrder(order=order)


def printOrderBook(self):
    print("Count\t\tVolume\t\t@ Price")
    for buyOrder in self.buyOrders:
        volume = 0;
        for orderId in self.buyOrdersDetails[buyOrder]:
            order = self.order_d[(self.order_d['Order_ID'] == orderId) & (self.order_d['Event'] == 1)]
            volume += order.volume

        print(len(self.buyOrdersDetails[buyOrder]), "\t\t", volume, "\t\t @", buyOrder)

    print("\n\n\n")
    print("Count\t\tVolume\t\t@ Price")
    for sellOrder in self.sellOrders:
        volume = 0;
        for orderId in self.sellOrdersDetails[sellOrder]:
            order = self.order_d[(self.order_d['Order_ID'] == orderId) & (self.order_d['Event'] == 1)]
            volume += order.volume

        print(len(self.sellOrdersDetails[sellOrder]), "\t\t", volume, "\t\t @", sellOrder)
