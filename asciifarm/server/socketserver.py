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
    
    
    def __init__(self, socketType, onConnection=(lambda *_:None), onMessage=(lambda *_:None), onConnectionClose=(lambda *_:None)):
        
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
        self.sel = selectors.DefaultSelector()
    
    
    def listen(self, address):
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
        
        self.sock.setblocking(False)
        
        self.sel.register(self.sock, selectors.EVENT_READ, "ACCEPT")
        
        self.connections = {}
        print("listening")
        while True:
            events = self.sel.select()
            for key, mask in events:
                if key.data == "ACCEPT":
                    sock = key.fileobj
                    connection, client_address = sock.accept()
                    connection.setblocking(False)
                    self.sel.register(connection, selectors.EVENT_READ, "RECEIVE")
                    self.connections[connection] = _BytesBuffer()
                    self.onConnection(connection)
                elif key.data == "RECEIVE":
                    connection = key.fileobj
                    data = connection.recv(4096)
                    if data:
                        buff = self.connections[connection]
                        buff.addBytes(data)
                        for message in buff.readMessages():
                            self.onMessage(connection, message)
                    else:
                        del self.connections[connection]
                        self.onConnectionClose(connection)
                    
            #listener = threading.Thread(target=self._listenCon, args=(connection,), daemon=True)
            #listener.start()
        
    
    #def _listenCon(self, connection):
        #self.connections.add(connection)
        #self.onConnection(connection)
        #data = receive(connection)
        #while data:
            #self.onMessage(connection, data)
            #try:
                #data = receive(connection)
            #except socket.error:
                #break
            #if not len(data):
                #break
        #self.connections.discard(connection)
        #self.onConnectionClose(connection)
    
    
    def getUsername(self, connection):
        
        if self.sockType != socket.AF_UNIX:
            return None
        
        peercred = connection.getsockopt(socket.SOL_SOCKET, socket.SO_PEERCRED, struct.calcsize("3i"))
        pid, uid, gid = struct.unpack("3i", peercred)
        import pwd
        return pwd.getpwuid(uid)[0]
    
    
    def send(self, connection, msg):
        try:
            length = len(msg)
            header = length.to_bytes(4, byteorder="big")
            connection.sendall(header + msg)
        except Exception:
            del self.connections[connection]
            self.onConnectionClose(connection)
            print("failed to send to client")
    
    def broadcast(self, msg):
        for connection in frozenset(self.connections):
            self.send(connection, msg)

