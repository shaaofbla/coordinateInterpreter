import socket
import rtmidi
import string
import time
import sys
from TCP.server import server
from MIDI.MidiOut import MidiOut
from MIDI.MidiNote import MidiNote
from MIDI.Midi import Midi
from MIDI.CC import CC


device= 'to Max 1'#to Max 1
Midi = Midi(device)
Midi.MidiOut.connectDevice()

previous_note_value = 0

TCPserver = server()
TCPserver.config()
TCPserver.listen()

def TCPmessage2coordinates(data_list):
	x,y,r = data_list
	return x,y,r

while True:
    try:
        TCPserver.connect()
        start_time = 0
        while 1:
            TCPserver.receive()
            if not TCPserver.data:
                break
            elapsed_time = time.time() - start_time
            fps = 1/elapsed_time
            print "FPS: ", fps

            start_time = time.time()
            data_list = string.split(TCPserver.data, "\t")
            if len(data_list) == 3:
                x,y,r = TCPmessage2coordinates(data_list)
                Xnote_value = int(float(x)/480*128)
                Ynote_value = int(float(y)/240*128)
                Xcontrol = Xnote_value
                Ycontrol = Ynote_value
            if Xnote_value != previous_note_value:
                velocity = int(float(y)/300*128)
                note = MidiNote(Xnote_value, velocity,10)
                Midi.appendNote(note)
                note = MidiNote(Ynote_value, velocity,10)
                Midi.appendNote(note)
                cc = CC(0x74, Xcontrol)
                Midi.appendCC(cc)
                cc = CC(0x75, Ycontrol)
                Midi.sendNotes()
                Midi.sendCCs()
                previous_note_value = Xnote_value
            else:
                next
            print "process", time.time()-start_time
    except KeyboardInterrupt:
        break
    TCPserver.close()
print "deleting midi object"
Midi.MidiOut.delet()
