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
            Xnote_value = int(float(XYRInterp.Object.x)/320*128)
            if Xnote_value != previous_note_value:
                XYRInterp.Object2Note()
                XYRInterp.SendAll()
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

