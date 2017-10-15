
import socket

from tcommunicate import send, receive

class Connection:
    
    def __init__(self):
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    
    def connect(self, address):
        self.sock.connect(address)
    
    def listen(self, callback, onError):
        while True:
            try:
                data = receive(self.sock)
            except Exception as err:
                onError(err)
            callback(data)
    
    def send(self, message):
        send(self.sock, bytes(message, 'utf-8'))
