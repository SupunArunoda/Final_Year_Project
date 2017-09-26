from dateutil import parser as DUp
from pandas import DataFrame, read_csv

from app.preprocess.Window.EventWindow import EventWindow


class PriceGapStaticByEvents:


    def __init__(self,session_file,no_of_events):

        self.attributes = DataFrame()

        self.first_order=None;
        self.first_buy_order = None;
        self.first_sell_order = None;
        self.sell_attributes = DataFrame()
        self.buy_attributes = DataFrame()
        self.temp_time=0
        self.count=0
        self.eventCount = 0
        self.no_of_events=no_of_events

        self.anomaly_first_point=DUp.parse("2016-04-29 13:02:00")
        self.anomaly_second_point = DUp.parse("2016-04-29 13:22:00")

        self.session = read_csv(session_file)
        self.regular_list=self.get_regular_time()
        self.window=EventWindow(no_of_events=no_of_events)


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
            if (temp_trasact_time>=self.regular_list[i] and temp_trasact_time<=self.regular_list[i + 1]):
                if self.window.isWindowLimitReach(order=order)==False:
                    self.get_calculation(order=order)
                else:
                    self.get_calculation(order=order)
                    self.normalize_df()
                    self.count=self.count+1
                    print(self.attributes)
                    self.write_csv(count=self.count)
                    self.first_order = None;
                    self.attributes=DataFrame()
                break


    def normalize_df(self):
        mean_price_gap=self.attributes['price_gap'].mean()

        std_price_gap=self.attributes['price_gap'].values.std(ddof=1)

        self.attributes['nom_price_gap']=(self.attributes['price_gap']-mean_price_gap)/std_price_gap

    def write_csv(self,count):
        self.attributes.to_csv("F:/Hishara/FYP/Final_Year_Project/app/output/price_gap_regular_"+str(count)+"_all.csv", index=False, encoding='utf-8')

    def get_calculation(self,order):
        if (self.first_order==None):
            if(order.execution_type==15):
                self.first_order=order.executed_value
            else:
                self.first_order = order.value
        else:
            if(order.execution_type==15):
                price_gap = order.executed_value - self.first_order
                self.first_order = order.executed_value
            else:
                price_gap = order.value - self.first_order
                self.first_order = order.value
            self.attributes = self.attributes.append(DataFrame({
                'time_index': order.transact_time,
                'price_gap': price_gap
                    }, index=[0]), ignore_index=True);




