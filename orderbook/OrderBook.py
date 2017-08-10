from pandas import DataFrame


class OrderBook:
    buyOrders = []
    sellOrders = []

    buyOrdersDetails = {}
    sellOrdersDetails = {}

    def __init__(self, order_data):
        self.order_d = order_data
        columns = ['instrument_id', 'broker_id', 'executed_value', 'value', 'transact_time', 'execution_type',
                   'order_qty', 'executed_qty', 'total_qty', 'side', 'visible_size', 'order_id']
        self.neworders = DataFrame(columns=columns)


    def processOrder(self, order):
        if(order.value>0):
            if order.execution_type == 0:
                self.addNewOrder(order)
            elif order.execution_type == 4:
                self.cancelOrder(order)
            elif order.execution_type == 5:
                self.amendOrder(order)
            elif order.execution_type == 15:
                self.executeOrder(order)

    def addNewOrder(self, order):
        #to keep track of total volume of a order
        tempDataFrame=self.neworders[(self.order_d['order_id'] == order.order_id) & (self.neworders['execution_type'] == 0)]
        if(tempDataFrame.count().iloc[0]==0):
            self.neworders = self.neworders.append(self.order_d[(self.order_d['order_id'] == order.order_id) & (self.order_d['execution_type'] == 0)], ignore_index=True);
        elif(tempDataFrame.count().iloc[0]>0):
            self.neworders.loc[((self.neworders['order_id'] == order.order_id) & (self.neworders['execution_type'] == 0)), 'visible_size'] += order.visible_size

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

    def executeOrder(self, order):
        if order.side == 1:  # if buy order
            price=self.neworders.loc[((self.order_d['order_id'] == order.order_id) & (self.neworders['execution_type'] == 0)),'value']
            if price.empty==False:
                tempOrder = self.neworders[(self.order_d['order_id'] == order.order_id) & (self.neworders['execution_type'] == 0)]
                volume = tempOrder['visible_size'].iloc[0]
                diff = (volume - order.visible_size)
                self.neworders.loc[((self.neworders['order_id'] == order.order_id) & (self.neworders['execution_type'] == 0)), 'visible_size'] = diff

                if diff == 0:
                    self.cancelOrder(order=order)

        else:  # if sell order
            price = self.neworders.loc[
                ((self.order_d['order_id'] == order.order_id) & (self.neworders['execution_type'] == 0)), 'value']
            if price.empty==False:
                tempOrder = self.neworders[(self.order_d['order_id'] == order.order_id) & (self.neworders['execution_type'] == 0)]
                volume = tempOrder['visible_size'].iloc[0]
                diff = (volume - order.visible_size)
                self.neworders.loc[((self.neworders['order_id'] == order.order_id) & (self.neworders['execution_type'] == 0)), 'visible_size'] = diff

                if diff == 0:
                    self.cancelOrder(order=order)

    def amendOrder(self, order):
        price=0
        price = self.neworders.loc[
            ((self.neworders['order_id'] == order.order_id) & (self.neworders['execution_type'] == 0)), 'value']
        if price.empty == False:
            self.neworders.loc[((self.neworders['order_id'] == order.order_id) & (self.neworders['execution_type'] == 0)), 'value'] = [order.value]
            self.neworders.loc[
                ((self.neworders['order_id'] == order.order_id) & (self.neworders['execution_type'] == 0)), 'transact_time'] = [
                order.transact_time]
            self.neworders.loc[
                ((self.neworders['order_id'] == order.order_id) & (self.neworders['execution_type'] == 0)), 'order_qty'] = [
                order.order_qty]
            self.neworders.loc[
                ((self.neworders['order_id'] == order.order_id) & (self.neworders['execution_type'] == 0)), 'total_qty'] = [
                order.total_qty]
            self.neworders.loc[
                ((self.neworders['order_id'] == order.order_id) & (self.neworders['execution_type'] == 0)), 'visible_size'] = [
                order.visible_size]

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
