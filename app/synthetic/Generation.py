from pandas import DataFrame, read_csv
from app.orderbook.Order import Order
from app.preprocess.window.EventWindow import EventWindow
from dateutil import parser as DUp
import random


class Generation:


    def __init__(self, session_file, window):
        self.temp_time = 0
        self.session = session_file
        self.regular_list = self.get_regular_time()
        self.all_attributes = DataFrame()
        self.type_df = []
        self.side_df = []
        self.start_times = []
        self.end_times = []
        self.window = window
        self.chunk = []
        self.count=0
        self.path = "D:/Acadamic/Final Year Research/Project/Final_Year_Project"
        # print(self.regular_list)


    def get_regular_time(self):
        count=0;
        reg_list=[]
        for index,session_row in self.session.iterrows():
            session_name=session_row['session_name']
            if(session_name[:15]=='Regular Trading'):
                reg_list.insert(count,DUp.parse(session_row['transact_time']))
                count+=1
        return reg_list

    def get_regular_gap_chunks(self, order):

        temp_trasact_time = DUp.parse(order.transact_time)
        for i in range(0, len(self.regular_list), 2):
            if (temp_trasact_time >= self.regular_list[i] and temp_trasact_time <= self.regular_list[i + 1]):
                if (self.window.isWindowLimitReach(order=order) == False):
                    self.all_attributes = self.all_attributes.append(DataFrame(
                        {'order_id': order.order_id,
                         'visible_size': order.visible_size,
                         'side': order.side,
                         'total_qty': order.total_qty,
                         'executed_qty': order.executed_qty,
                         'order_qty': order.order_qty,
                         'execution_type': order.execution_type,
                         'transact_time': order.transact_time,
                         'value': order.value,
                         'executed_value': order.executed_value,
                         'broker_id': order.broker_id,
                         'instrument_id': order.instrument_id,
                         }, index=[0]), ignore_index=True);
                    if (self.temp_time == 0):
                        self.temp_time = temp_trasact_time
                else:
                    self.count = self.count + 1
                    self.write_csv(count=self.count)
                    self.temp_time = 0
                    self.first_order = None;
                    self.temp_time = temp_trasact_time


    def write_csv(self, count):
        self.all_attributes.to_csv(self.path+"/app/output/synthetic_data/all_attributes_" + str(count) + ".csv",
                                   index=False, encoding='utf-8')
        self.all_attributes = DataFrame()

def mapping(percentage,no_of_lines_anomaly,file_count):
    temp_rnad = random.randint(1, file_count);
    normal_data=read_csv("D:/Acadamic/Final Year Research/Project/Final_Year_Project/app/output/synthetic_data/normal/all_attributes_" + str(7) + ".csv")
    anomlay_data=read_csv("D:/Acadamic/Final Year Research/Project/Final_Year_Project/app/output/synthetic_data/anomaly/all_attributes_" + str(7) + ".csv")
    no_lines=int(percentage*no_of_lines_anomaly)#no of lines in percentage
    rand_gen_for_anomaly=random.randint(1,no_of_lines_anomaly/no_lines)#to get where to add anomaly
    rand_gen_for_normal=random.randint(1,no_of_lines_anomaly/no_lines)
    #print(str("rnadom numbers"),rand_gen_for_normal,rand_gen_for_anomaly)
    start_point_anomaly=0#(rand_gen_for_anomaly-1)*no_lines
    end_point_anomaly = 1000#(rand_gen_for_anomaly) * no_lines
    start_point_normal = 0#(rand_gen_for_normal - 1) * no_lines
    end_point_normal = (rand_gen_for_normal) * no_lines
    print(start_point_anomaly,end_point_anomaly,start_point_normal,end_point_normal,temp_rnad)

    i=0
    new_df=DataFrame()
    for index, order_row in normal_data.iterrows():
        if(index>start_point_anomaly and index<end_point_anomaly):
            #order_id = anomlay_data.ix[start_point_anomaly + (i)]['order_id']
            #broker_id = anomlay_data.ix[start_point_anomaly + (i)]['broker_id']
            value = anomlay_data.ix[start_point_anomaly + (i)]['value']
            visible_size = anomlay_data.ix[start_point_anomaly + (i)]['visible_size']
            side = anomlay_data.ix[start_point_anomaly + (i)]['side']
            total_qty = anomlay_data.ix[start_point_anomaly + (i)]['total_qty']
            executed_qty = anomlay_data.ix[start_point_anomaly + (i)]['executed_qty']
            order_qty = anomlay_data.ix[start_point_anomaly + (i)]['order_qty']
            execution_type = anomlay_data.ix[start_point_anomaly + (i)]['execution_type']
            executed_value = anomlay_data.ix[start_point_anomaly + (i)]['executed_value']
            #instrument_id = anomlay_data.ix[start_point_anomaly + (i)]['instrument_id']
            new_df = new_df.append(DataFrame(
                {'order_id': order_row['order_id'],
                 'visible_size': visible_size,
                 'side': side,
                 'total_qty': total_qty,
                 'executed_qty': executed_qty,
                 'order_qty': order_qty,
                 'execution_type': execution_type,
                 'transact_time': order_row['transact_time'],
                 'value': value,
                 'executed_value': executed_value,
                 'broker_id': order_row['broker_id'],
                 'instrument_id': order_row['instrument_id'],
                 }, index=[0]), ignore_index=True);
        else:
            new_df = new_df.append(DataFrame(
                {'order_id': order_row['order_id'],
                 'visible_size': order_row['visible_size'],
                 'side': order_row['side'],
                 'total_qty': order_row['total_qty'],
                 'executed_qty': order_row['executed_qty'],
                 'order_qty': order_row['order_qty'],
                 'execution_type': order_row['execution_type'],
                 'transact_time': order_row['transact_time'],
                 'value': order_row['value'],
                 'executed_value': order_row['executed_value'],
                 'broker_id': order_row['broker_id'],
                 'instrument_id': order_row['instrument_id'],
                 }, index=[0]), ignore_index=True);

        new_df.to_csv("D:/Acadamic/Final Year Research/Project/Final_Year_Project/app/output/synthetic_data/all_attributes_inject_7.csv",
                               index=False, encoding='utf-8')











def run():
    data = read_csv("D:/Acadamic/Final Year Research/Project/Final_Year_Project/app/data/data.csv")
    session=read_csv("D:/Acadamic/Final Year Research/Project/Final_Year_Project/app/data/sessions.csv")
    window=EventWindow(no_of_events=5000)
    gen=Generation(session_file=session,window=window)
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
        if order.value > 0:
            gen.get_regular_gap_chunks(order=order)

mapping(percentage=0.2,no_of_lines_anomaly=5000,file_count=10)

# run()



