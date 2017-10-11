import rtmidi
from numpy import where

class MidiOut:
    def __init__(self,device):
        self.Port = 0
        self.Device = device
        self.Output = rtmidi.MidiOut()

    def getDevicePort(self):
        available_ports = self.Output.get_ports()
        #available_ports = [x.encode('UTF8') for x in available_ports]
        try:
            self.Port = available_ports.index(self.Device)
        except ValueError:
            print "[MidiOut] No Device named {0}".format(self.Device)
            print "[MidiOut] Available ports: {0}".format(available_ports)
            return

    def connectDevice(self):
        print "[MidiOut] Connecting to {0}".format(self.Device)
        self.getDevicePort()
        self.connectPort()

    def connectPort(self):
        self.Output.open_port(self.Port)

    def send(self,message):
        self.Output.send_message(message)

    def delet(self):
        del self.Output
