from app.preprocess.window.Window import Window


class EventWindow(Window):

    def __init__(self , no_of_events):
        self.eventCount = 0
        self.no_of_events=no_of_events


    def isWindowLimitReach(self , order):
        self.eventCount+=1
        if(self.eventCount==self.no_of_events):
                self.eventCount = 0
                return True
        return False

    def isFirst(self):
        if self.eventCount==0:
            return True
        return False