from app.preprocess.window.Window import Window
import datetime
from dateutil import parser as DUp

#Analyze the time window
class TimeWindow:
    def __init__(self , time_delta):
        self.eventCount=0
        self.const_time_gap = datetime.timedelta(0, time_delta)
        self.windowStartTime = 0


    def isWindowLimitReach(self , order):
        self.eventCount+=1
        trasact_time = DUp.parse(order.transact_time)
        if(self.eventCount==1):
            self.windowStartTime=trasact_time
        tempTime=trasact_time-self.windowStartTime
        if(tempTime<=self.const_time_gap):
            return False
        else:
            self.eventCount =0
            self.windowStartTime=trasact_time
            return True

    def isFirst(self):
        if self.eventCount==0:
            return True
        return False