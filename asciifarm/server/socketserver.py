import os
import socket
import sys
import threading

from .tcommunicate import send, receive


# Class to open a TCP Socket
# will execute callback functions on new connections, closing connections and received messages
# also provides a send function

class Server:
    
    
    def __init__(self, socketType, onConnection=(lambda *_:None), onMessage=(lambda *_:None), onConnectionClose=(lambda *_:None)):
        
        if socketType == "abstract" or socketType == "unix":
            sockType = socket.AF_UNIX
        elif socketType == "inet":
            sockType = socket.AF_INET
        else:
            raise ValueError("invalid socket type "+str(socketType))
        self.sock = socket.socket(sockType, socket.SOCK_STREAM)
        self.socketType = socketType
        self.onConnection = onConnection
        self.onMessage = onMessage
        self.onConnectionClose = onConnectionClose
    
    
    def start(self, address):
        print("starting {} socket server on address {}".format(self.socketType, address))
        try:
            self.sock.bind(address)
        except PermissionError:
            print("You don't have permission to use this socket file.\nRun the server with the '-s' option to specify another socket file path.\nWARNING: if an existing file is given, it will be overwritten.")
            sys.exit(-1)
        except OSError:
            print("Unable to bind to the socket address.\nMost likely this means that a server is already running and using the same address.\n Try another socket address (and tell all players to connect to that)")
            sys.exit(-1)
        
        self.sock.listen()
        
        self.listener = threading.Thread(target=self._listen, daemon=True)
        self.listener.start()
    
    
    def _listen(self):
        self.connections = set()
        print("listening")
        while True:
            connection, client_address = self.sock.accept()
            listener = threading.Thread(target=self._listenCon, args=(connection,), daemon=True)
            listener.start()
    
    def _listenCon(self, connection):
        #print(connection.getsockopt(socket.SOL_SOCKET, socket.SO_PEERCRED))
        self.connections.add(connection)
        self.onConnection(connection)
        data = receive(connection)
        while data:
            self.onMessage(connection, data)
            try:
                data = receive(connection)
            except socket.error:
                break
            if not len(data):
                break
        self.connections.discard(connection)
        self.onConnectionClose(connection)
    
    
    
    def send(self, connection, msg):
        try:
            send(connection, msg)
        except:
            self.connections.discard(connection)
            self.onConnectionClose(connection)
            print("failed to send to client")
    
    def broadcast(self, msg):
        for connection in frozenset(self.connections):
            self.send(connection, msg)

