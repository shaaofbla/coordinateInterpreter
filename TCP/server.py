import socket
import utils.coordinateInterpreterConfig as config

class server:
    def __init__(self, ip= '192.168.0.11', port = 5005, buffer_size=60):
        self.ip = ip
        self.port = port
        self.buffer_size = buffer_size
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn = None
        self.addr = None
        self.data = False

    def config(self):
        self.ip = config.TCP_IP
        self.port = config.TCP_PORT
        self.buffer_size = config.BUFFER_SIZE

    def listen(self):
        self.socket.bind((self.ip,self.port))
        self.socket.listen(True)

    def connect(self):
        print "[TCPServer] Waiting for for client to connect"
        self.conn, self.addr = self.socket.accept()
        print "[TCPServer] Connected to address: {0}".format(self.ip)

    def receive(self):
        self.data = self.conn.recv(self.buffer_size)

    def close(self):
        self.conn.close()
