import socket
import time
from TCP.server import server
from XYRInterpreter.XYRInterpreter import XYRInterp

XYRInterp = XYRInterp()
XYRInterp.setupMidi()
XYRInterp.setupTCPserver()
previous_note_value = 0

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
            XYRInterp.interpret()
            print "time to interp", time.time()-start_time
            XYRInterp.SendAll()
            XYRInterp.Dims = []
            XYRInterp.Dimensions = []
            XYRInterp.TCPserver.data = False
            print "process", time.time()-start_time
    except KeyboardInterrupt:
        break
    XYRInterp.TCPserver.close()
print "deleting midi object"
XYRInterp.Midi.MidiOut.delet()

