from MidiOut import MidiOut
#from Object import Object
from MidiNote import MidiNote
import time

class Midi:
    def __init__(self,device):
        self.MidiOut = MidiOut(device)
        self.Notes = []
        self.CCs = []

    def sendNotes(self):
        for note in self.Notes:
            message = [note.On, note.value, note.velocity]
            self.MidiOut.send(message)
        time.sleep(0.001)
        for note in self.Notes:
            message = [note.Off, note.value,0]
            self.MidiOut.send(message)
        self.Notes = []

    def appendNote(self,midiNote):
        self.Notes.append(midiNote)

    def sendCCs(self):
        for cc in self.CCs:
            message = [cc.hexMessg, cc.channel, cc.change]
            self.MidiOut.send(message)
        self.CCs = []

    def appendCC(self,CC):
        self.CCs.append(CC)

