class CC:
    def __init__(self,channel,change):
        self.channel = channel
        self.change = change
        self.hexMessg = 0xb0

        def setChannel(self, channel):
            print isinstance(channel, int)
            print isinstance(channel, hex)
