import socket
#import rtmidi
#import string
import time
#import sys
from TCP.server import server
from MIDI.MidiOut import MidiOut
from MIDI.MidiNote import MidiNote
from MIDI.Midi import Midi
from MIDI.CC import CC
from XYRInterpreter.XYRInterpreter import XYRInterp


XYRInterp = XYRInterp()
XYRInterp.setupMidi()
XYRInterp.setupTCPserver()
previous_note_value = 0


def TCPmessage2coordinates(data_list):
	x,y,r = data_list
	return x,y,r

while True:
    try:
        XYRInterp.TCPserver.connect()
        start_time = 0
        while 1:
            XYRInterp.TCPserver.receive()
            if not XYRInterp.TCPserver.data:
                break
            elapsed_time = time.time() - start_time
            fps = 1/elapsed_time
            print "FPS: ", fps

            start_time = time.time()
            XYRInterp.TCPmessage2Object()
            Xnote_value = int(float(XYRInterp.Object.x)/480*128)
            Ynote_value = int(float(XYRInterp.Object.y)/240*128)
            Xcontrol = Xnote_value
            Ycontrol = Ynote_value
            if Xnote_value != previous_note_value:
                velocity = int(float(XYRInterp.Object.y)/300*128)
                note = MidiNote(Xnote_value, velocity,10)
                XYRInterp.Midi.appendNote(note)
                note = MidiNote(Ynote_value, velocity,10)
                XYRInterp.Midi.appendNote(note)
                cc = CC(0x74, Xcontrol)
                XYRInterp.Midi.appendCC(cc)
                cc = CC(0x75, Ycontrol)
                XYRInterp.Midi.sendNotes()
                XYRInterp.Midi.sendCCs()
                previous_note_value = Xnote_value
            else:
                next
            XYRInterp.TCPserver.data = False
            print "process", time.time()-start_time
    except KeyboardInterrupt:
        break
    XYRInterp.TCPserver.close()
print "deleting midi object"
XYRInterp.Midi.MidiOut.delet()

