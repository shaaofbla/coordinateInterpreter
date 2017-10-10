import socket
import rtmidi
import string
import time
import sys

midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()
print available_ports
port = 0
if available_ports:
    
	midiout.open_port(port)
else:
	midiout.open_virtual_port("Virtual Port")

previous_note_value = 0

TCP_IP = '192.168.0.11'#your own IP
TCP_PORT = 5005
BUFFER_SIZE = 60  # Normally 1024, but we want fast response

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

def TCPmessage2coordinates(data_list):
	x,y,r = data_list
	return x,y,r

conn, addr = s.accept()
print 'Connection address:', addr
start_time = 0
while 1:
    data = conn.recv(BUFFER_SIZE)
    if not data:
        break
    elapsed_time = time.time() - start_time
    fps = 1/elapsed_time
    print fps

    start_time = time.time()
    data_list = string.split(data, "\t")
    if len(data_list) == 3:
	x,y,r = TCPmessage2coordinates(data_list)
    Xnote_value = int(float(x)/480*128)
    Ynote_value = int(float(y)/240*128)
    Xcontrol = Xnote_value
    Ycontrol = Ynote_value
    if Xnote_value != previous_note_value:
        velocity = int(float(y)/300*128)
        Xnote_on = [0X90, Xnote_value, velocity]
        Xnote_off = [0X80, Xnote_value, 0]
        Ynote_on = [0x91, Ynote_value, velocity]
        Ynote_off = [0x80, Ynote_value, 0]
        Xcontrol = [0xb0, 0x74, Xcontrol]
        Ycontrol = [0xb0, 0x75, Ycontrol]
        midiout.send_message(Xnote_on)
        midiout.send_message(Ynote_on)
        time.sleep(0.001)
        midiout.send_message(Ynote_off)
        midiout.send_message(Xnote_off)
        midiout.send_message(Xcontrol)
        midiout.send_message(Ycontrol)
        previous_note_value = Xnote_value
    else:
	next
conn.close()
del midiout
