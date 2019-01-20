#! /usr/bin/python3


import json
import queue
import string

from . import view
from . import socketserver as server
from . import player


class GameServer:
    
    
    def __init__(self, game, socketType):
        
        self.serv = server.Server(socketType, self.newConnection, self.receive, self.close)
        
        self.connections = {}
        
        self.players = {}
        
        self.game = game
        
        self.messages = queue.Queue()
    
    def start(self, address):
        self.serv.start(address)
    
    def sendState(self, view):
        
        for connection, name in list(self.connections.items()):
            data = view.playerView(name)
            if data is None:
                continue
            databytes = bytes(json.dumps(data), 'utf-8')
            
            self.serv.send(connection, databytes)
    
    def newConnection(self, n):
        pass
    
    def receive(self, n, data):
        try:
            data = json.loads(data.decode('utf-8'))
            if isinstance(data[0], str):
                data = [data]
            for msg in data:
                msgType = msg[0]
                if msgType == "name":
                    name = msg[1]
                    
                    if name in self.players:
                        self.error(n, "nametaken", "another connection to this player already exists")
                        return
                    if len(name) < 1:
                        self.error(n, "invalidname", "name needs at least one character")
                        return
                    if name[0] not in string.ascii_letters + string.digits:
                        if name[0] != "~":
                            self.error(n, "invalidname", "custom name must start with an alphanumeric character")
                            return
                        if name[1:] != self.serv.getUsername(n):
                            self.error(n, "invalidname", "tildenames are only available on unix sockets and when the rest of the name equals the username")
                            return
                    if any(char not in string.ascii_letters + string.digits + string.punctuation for char in name):
                        self.error(n, "invalidname", "names can only consist of printable ascii characters")
                        return
                    self.connections[n] = name
                    self.players[name] = n
                    self.messages.put(("join", name))
                    print("new player: "+name)
                    self.broadcast("{} has connected".format(name), "connect")
                    return
                elif msgType == "input":
                    if n in self.connections:
                        self.messages.put(("input", self.connections[n], msg[1]))
                elif msgType == "chat":
                    if n in self.connections:
                        name = self.connections[n]
                        message = name + ": " + msg[1]
                        print(message)
                        self.broadcast(message, "chat")
        
        except Exception as e:
            print(e)
            self.error(n, "invalidmessage", repr(e))
    
    
    def error(self, n, errtype, *data):
        self.serv.send(n, bytes(json.dumps(["error", errtype]+list(data)), "utf-8"))
    
    def close(self, connection):
        if connection in self.connections:
            name = self.connections[connection]
            del self.connections[connection]
            del self.players[name]
            self.messages.put(("leave", name))
            print("player "+name+" left")
            self.broadcast("{} has disconnected".format(name), "connect")
    
    def broadcast(self, message, type="server"):
        databytes = bytes(json.dumps(["message", message, type]), "utf-8")
        for connection in self.connections:
            self.serv.send(connection, databytes)
        
    
    def readMessages(self):
        m = []
        while not self.messages.empty():
            m.append(self.messages.get())
        return m



