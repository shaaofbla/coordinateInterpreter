import numpy as np

class CC:
    def __init__(self,Repeater):
        self.Messages = np.empty(0)
        self.Repeater = Repeater
        self.NbrMessages = sum(Repeater)
        self.HexMessages = np.repeat(0xb0,self.NbrMessages).astype(int)
        self.previousControlChange = np.empty(self.NbrMessages)


