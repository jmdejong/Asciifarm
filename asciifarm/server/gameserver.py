#! /usr/bin/python3


import json
import queue
import string
import threading


from . import view
from . import socketserver as server
from . import player

import re

nameRegex = re.compile("(~|\w)\w*")

class GameServer:
    
    
    def __init__(self, socketType, address):
        
        self.serv = server.Server(socketType, address, self.newConnection, self.receive, self.close)
        
        self.connections = {}
        self.players = {}
        self.messages = queue.Queue()
    
    def start(self):
        
        self.listener = threading.Thread(target=self.serv.listen, daemon=True)
        self.listener.start()
    
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
            try:
                data = json.loads(data.decode('utf-8'))
            except json.JSONDecodeError:
                self.error(n, "invalidmessage", "Invalid JSON")
                return
            if not isinstance(data, list) or len(data) != 2:
                self.error(n, "invalidmessage", "Message must be a json list of length 2")
                return
            msg = data
            msgType = msg[0]
            if msgType == "name":
                name = msg[1]
                
                if len(name) < 1:
                    self.error(n, "invalidname", "name needs at least one character")
                    return
                if len(bytes(name, "utf-8")) > 256:
                    self.error(n, "invalidname", "name may not be longer than 256 utf8 bytes")
                    return
                if nameRegex.match(name) is None:
                    self.error(n, "invalidname", "Name must match the following regex: {}".format(nameRegex.pattern))
                    return
                if name[0] == "~" and name[1:] != self.serv.getUsername(n):
                    self.error(n, "invalidname", "tildenames are only available on unix sockets and when the rest of the name equals the username")
                    return
                if name in self.players:
                    self.error(n, "nametaken", "another connection to this player already exists")
                    return
                self.connections[n] = name
                self.players[name] = n
                self.messages.put(("join", name))
                print("new player: "+name)
                self.broadcast("{} has connected".format(name), "connect")
            elif msgType == "input":
                if n in self.connections:
                    self.messages.put(("input", self.connections[n], msg[1]))
            elif msgType == "chat":
                if n in self.connections:
                    name = self.connections[n]
                    if not msg[1].isprintable():
                        self.error("invalidmessage", "Chat message may only contain printable unicode characters")
                    message = name + ": " + msg[1]
                    print(message)
                    self.broadcast(message, "chat")
        
        except Exception as e:
            print(e)
            self.error(n, "invalidmessage", "An unknown error occured in handling the message")
    
    
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
            try:
                message = self.messages.get_nowait()
            except queue.Empty:
                return m
            m.append(message)
        return m



