
import socket

from asciifarm.common.tcommunicate import send, receive

class Connection:
    
    def __init__(self, socketType):
        if socketType == "abstract" or socketType == "unix":
            sockType = socket.AF_UNIX
        elif socketType == "inet":
            sockType = socket.AF_INET
        self.sock = socket.socket(sockType, socket.SOCK_STREAM)
    
    def connect(self, address):
        self.sock.connect(address)
    
    def listen(self, callback, onError):
        while True:
            try:
                data = receive(self.sock)
            except Exception as err:
                onError(err)
            else:
                callback(data)
    
    def send(self, message):
        send(self.sock, bytes(message, 'utf-8'))
