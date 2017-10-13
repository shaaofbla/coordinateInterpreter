from MidiOut import MidiOut
from CC import CC
from MidiNote import MidiNote
import utils.XYRInterpConfig as config
import time
import numpy as np

class Midi:
    def __init__(self,device=None):
        self.MidiOut = MidiOut(device)
        self.Notes = []
        self.CC = CC(config.CC_REPEATER)

    def config(self):
        self.MidiOut.Device = config.MIDI_DEVICE

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
        if self.CC.Messages.size == 0:
            return
        else:
            print "sending"
            np.apply_along_axis(self.sendCC,axis = 1, arr=self.CC.Messages)
            self.CC.Messages = np.empty(0)
            return

    def sendCC(self,msg):
        self.MidiOut.send(msg.tolist())
        return 1

    def getNewCCs(self,repeatedInput, mappings):
        new = scaleMatrix(repeatedInput, mappings)
        new = new.astype(int)
        return new

    def input2outputDistributor(self,Dim):
        out = np.repeat(Dim,self.CC.Repeater,axis=0).astype(int)
        return out

    def makeCCs(self, Dim, mappings):
        self.CC.MidiChannels = mappings[:,4].astype(int)
        distributedInput = self.input2outputDistributor(Dim)
        newControlChange = self.getNewCCs(distributedInput, mappings)
        controlChange_Changes = newControlChange != self.CC.previousControlChange
        CCmessage = np.transpose(np.vstack((self.CC.HexMessages,self.CC.MidiChannels,newControlChange)))
        CCmessage = CCmessage[controlChange_Changes,:]
        self.CC.Messages = CCmessage
        self.CC.previousControlChange = newControlChange

def scaleMatrix(Input, mapping):
    inMin = mapping[:,0]
    inMax = mapping[:,1]
    outMin = mapping[:,2]
    outMax = mapping[:,3]
    inRange = inMax - inMin
    outRange = outMax - outMin
    res = (((Input - inMin) * outRange) / inRange) + outMin
    return res
