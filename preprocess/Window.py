from pandas import DataFrame,read_csv
from datetime import datetime
from dateutil import parser as DUp

class Window:


    def __init__(self,session_file):

        self.attributes = DataFrame()
        self.temp_time=0;
        self.session = read_csv(session_file)
        self.regular_list=[]

    def get_regular_time(self):
        count=0;
        for index,session_row in self.session.iterrows():
            session_name=session_row['session_name']
            if(session_name[:15]=='Regular Trading'):
                self.regular_list.insert(count,DUp.parse(session_row['transact_time']))
                count+=1
        return self.regular_list

    def get_time_frame(self,order):
        reg_list=self.get_regular_time()
        for i in range(len(reg_list)):
            if(order.transact_time>=reg_list[i] and order.transact_time<=reg_list[i+1]):
                self.attributes = self.attributes.append(DataFrame(
                    {'order_id': order.order_id, 'value': order.value, 'visible_size': order.visible_size,}
                    , index=[0]), ignore_index=True);
            i+=2;
        return self.attributes;

