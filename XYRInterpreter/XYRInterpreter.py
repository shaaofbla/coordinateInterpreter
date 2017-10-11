from utils.Object import Object
from MIDI.Midi import Midi
from MIDI.MidiNote import MidiNote
from TCP.server import server
import string

class XYRInterp:
    def __init__(self):
        self.Object = Object()
        self.Midi = Midi()
        self.TCPserver = server()

    def setupMidi(self):
        self.Midi.config()
        self.Midi.MidiOut.connectDevice()

    def setupTCPserver(self):
        self.TCPserver.config()
        self.TCPserver.listen()

    def TCPmessage2Object(self):
        data_list = string.split(self.TCPserver.data, "\t")
        if len(data_list) == 4:
            print data_list.pop()
            x,y,r = data_list
            self.Object.x = x
            self.Object.y = y
            self.Object.r = r
        else :
            raise ValueError("The data from the TCP client contained some strange things")

    def Object2Note(self):
        Xnote_value = int(float(self.Object.x)/320*128)
        Ynote_value = int(float(self.Object.y)/240*128)
        velocity = int(float(self.Object.y)/240*128)
        note = MidiNote(Xnote_value, velocity, 10)
        self.Midi.appendNote(note)
        note = MdidNote(Ynote_value, velocity,10)
        self.Midi.appendNote(note)

    def Object2CC(self):
        Xcontrol = int(float(self.Object.x)/320*128)
        Yconrtol = int(float(self.Object.y)/240*128)
        cc = CC(0x74, Xcontrol)
        self.Midi.appendCC(cc)
        cc = CC(0x75, Ycontrol)
        self.Midi.appendCC(cc)

    def SendAll(self):
        self.Interp.Midi.sendNotes()
        self.Midi.sendCCs()
        
