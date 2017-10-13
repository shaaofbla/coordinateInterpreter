from utils.Dimensions import Dim
from utils.Coords import Coords
from MIDI.Midi import Midi
from utils.XYRInterpConfig import CC_REPEATER
from MIDI.MidiNote import MidiNote
from MIDI.CC import CC
from TCP.server import server
import numpy as np
import string
import time

class XYRInterp:
    def __init__(self):
        self.Dims = []
        self.Dimensions = []
        self.Midi = Midi()
        self.Coords = Coords()
        self.TCPserver = server()
        self.CameraResolution = (320,240)
        self.mappingFile = "./utils/mappingsTest.txt"
        self.mapping = np.loadtxt(self.mappingFile,skiprows=1)

    def setupMidi(self):
        self.Midi.config()
        self.Midi.MidiOut.connectDevice()

    def setupTCPserver(self):
        self.TCPserver.config()
        self.TCPserver.listen()

    def setCoords(self,data_list):
        if len(data_list) == 4:
            data_list.pop()
            x,y,r = data_list
            self.Coords.x = float(x)
            self.Coords.y = float(y)
            self.Coords.r = float(r)

        elif len(data_list) > 4:
            data_list = data_list[-4:]
            self.setCoords(data_list)
        else:
            raise ValueError("The data from TCP client contained some strange things: {0}".format(data_list))

    def TCPmessage2Coords(self):
        data_list = string.split(self.TCPserver.data, "\t")
        self.setCoords(data_list)

    def Coords2Dims(self):
        self.Dims.append(Dim("x",self.Coords.x,0,self.CameraResolution[0]))
        self.Dimensions.append(self.Coords.x)
        self.Dims.append(Dim("y",self.Coords.y,0,self.CameraResolution[1]))
        self.Dimensions.append(self.Coords.y)
        self.Dims.append(Dim("r",self.Coords.r,0, 100))
        self.Dimensions.append(self.Coords.r)

    def centerXY(self):
        x_center = self.Coords.x - (self.CameraResolution[0]/2)
        y_center = self.Coords.y - (self.CameraResolution[1]/2)
        return x_center, y_center

    def addPolar2Dims(self):
        x_center, y_center = self.centerXY()
        print "xcent", x_center,"ycent", y_center
        rho,phi = cartesian2polar(x_center,y_center)
        print "rho", rho,"phi", phi
        #phi = np.abs(phi) ###!!!
        self.Dims.append(Dim("rho",rho,0,self.CameraResolution[1]/2))
        self.Dimensions.append(rho)
        self.Dims.append(Dim("phi",phi,0, 360))
        self.Dimensions.append(phi)

    def collectDims(self):
        self.Coords2Dims()
        self.addPolar2Dims()

    def interpret(self):
        start_time = time.time()
        self.TCPmessage2Coords()
        tcpmesg2coords_time = time.time()
        print "[interp] TCpmessg2coord", tcpmesg2coords_time-start_time
        self.collectDims()
        collcgDim_time = time.time()
        print "[interp] Collectdims",collcgDim_time-tcpmesg2coords_time
        #self.Dim2Notes()
        dim2notes_time = time.time()
        print "[interp] dimtonotes", dim2notes_time-collcgDim_time
        self.Coords2CCs()
        coords2CC_time = time.time()
        print "[interp] coords2CC",  coords2CC_time-dim2notes_time

    def Dim2Notes(self):
        #Slow!! maybe use matrices to scale the values
        for dim in self.Dims:
            note = self.scale_Dim2Midi(dim,0, 127)
            velocity = 80
            duration = 10
            self.Midi.appendNote(MidiNote(note, velocity,duration))

    def scale_Dim2Midi(self,Dim,outMin,outMax):
        dimRange = Dim.max - Dim.min
        outRange = outMax-outMin
        res = (((Dim.val-Dim.min) * outRange) / dimRange)+outMin
        return int(res)

    def Coords2CCs(self):
        self.Midi.makeCCs(self.Dimensions,self.mapping)

    def SendAll(self):
        #self.Midi.sendNotes()
        self.Midi.sendCCs()

def cartesian2polar(x,y):
    rho = np.sqrt(x**2 + y**2)
    phi = np.degrees(np.arctan2(y, x))
    return rho, phi


