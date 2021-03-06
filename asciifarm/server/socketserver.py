import os
import socket
import sys
import struct
import selectors

from asciifarm.common.tcommunicate import send, receive


class _BytesBuffer:
    
    def __init__(self):
        self.buff = bytearray()
        self.msglen = None
    
    def addBytes(self, data):
        self.buff.extend(data)
    
    def readMessages(self):
        messages = []
        while True:
            if self.msglen is None:
                if len(self.buff) < 4:
                    break
                header = self.buff[:4]
                self.msglen = int.from_bytes(header, byteorder="big")
                self.buff = self.buff[4:]
            elif len(self.buff) >= self.msglen:
                messages.append(self.buff[:self.msglen])
                self.buff = self.buff[self.msglen:]
                self.msglen = None
            else:
                break
        return messages

# Class to open a TCP Socket
# will execute callback functions on new connections, closing connections and received messages
# also provides a send function

class Server:
    
    
    def __init__(self, socketInfo, onConnection=(lambda *_:None), onMessage=(lambda *_:None), onConnectionClose=(lambda *_:None)):
        
        socketType, address = socketInfo
        
        if socketType == "abstract" or socketType == "unix":
            self.sockType = socket.AF_UNIX
        elif socketType == "inet":
            self.sockType = socket.AF_INET
        else:
            raise ValueError("invalid socket type "+str(socketType))
        self.sock = socket.socket(self.sockType, socket.SOCK_STREAM)
        self.socketType = socketType
        self.onConnection = onConnection
        self.onMessage = onMessage
        self.onConnectionClose = onConnectionClose
        self.address = address
        self.selector = None
    
    
    def listen(self, selector):
        try:
            self.sock.bind(self.address)
        except PermissionError:
            print("You don't have permission to use this socket file.\nRun the server with the '-s' option to specify another socket file path.\nWARNING: if an existing file is given, it will be overwritten.")
            sys.exit(-1)
        except OSError:
            print("Unable to bind to the {} socket address '{}'.\nMost likely this means that a server is already running and using the same address.\n Try another socket address (and tell all players to connect to that)".format(self.socketType, self.address))
            sys.exit(-1)
        
        self.sock.listen()
        
        self.sock.setblocking(False)
        
        self.selector = selector
        
        selector.register(self.sock, selectors.EVENT_READ, self._accept)
        
        self.connections = {}
        print("started {} socket server on address {}".format(self.socketType, self.address))
    
    def _accept(self, sock, selector):
            connection, client_address = sock.accept()
            connection.setblocking(False)
            selector.register(connection, selectors.EVENT_READ, self._receive)
            self.connections[connection] = _BytesBuffer()
            self.onConnection((self, connection))
    
    def _receive(self, connection, selector):
            try:
                data = connection.recv(4096)
            except ConnectionResetError:
                data = None
            if data:
                buff = self.connections[connection]
                buff.addBytes(data)
                for message in buff.readMessages():
                    self.onMessage((self, connection), message)
            else:
                self.closeConnection(connection)
    
    def closeConnection(self, connection):
        try:
            del self.connections[connection]
        except KeyError:
            return
        connection.close()
        self.selector.unregister(connection)
        self.onConnectionClose((self, connection))
    
    def getUsername(self, connection):
        
        if self.sockType != socket.AF_UNIX:
            return None
        
        peercred = connection.getsockopt(socket.SOL_SOCKET, socket.SO_PEERCRED, struct.calcsize("3i"))
        pid, uid, gid = struct.unpack("3i", peercred)
        import pwd
        return pwd.getpwuid(uid)[0]
    
    
    def send(self, connection, msg):
        if connection in self.connections:
            length = len(msg)
            header = length.to_bytes(4, byteorder="big")
            try:
                connection.sendall(header + msg)
            except (BrokenPipeError, OSError):
                self.closeConnection(connection)
    
    def broadcast(self, msg):
        for connection in frozenset(self.connections):
            self.send(connection, msg)

