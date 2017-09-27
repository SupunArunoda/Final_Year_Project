class Window:
    def __init__(self , no_of_events):
        self.eventCount = 0
        self.no_of_events=no_of_events


    def isWindowLimitReach(self , order):
        raise NotImplementedError("Should have implemented this")

    def isFirst(self):
        raise NotImplementedError("Should have implemented this")