#! /usr/bin/python3


import json
import queue
import string
import threading


from . import view
from . import socketserver as server
from . import player

from asciifarm.common import messages

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
            databytes = bytes(json.dumps(["world", data]), 'utf-8')
            
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
            if not isinstance(msgType, str):
                self.error(n, "invalidmessage", "Message type must be a string")
                return
            msgClass = messages.messages.get(msgType)
            if msgClass is None:
                self.error(n, "invalidmessage", "Unknown message type '{}'".format(msgType))
                return
            try:
                message = msgClass.from_json(msg)
            except messages.InvalidMessageError as e:
                self.error(n, e.errType, e.description)
                return
            
            self.handleMessage(n, message)
            
        
        except Exception as e:
            print(e)
            self.error(n, "invalidmessage", "An unknown error occured in handling the message")
    
    def handleMessage(self, n, message):
        # I wish I had type overloading
        if isinstance(message, messages.NameMessage):
            self.handleNameMessage(n, message)
        elif isinstance(message, messages.InputMessage):
            self.handleInputMessage(n, message)
        elif isinstance(message, messages.ChatMessage):
            self.handleChatMessage(n, message)
        else:
            self.error(n, "invalidmessage", "unknown message '{}'".format(message.__class__))
    
    
    def handleNameMessage(self, n, message):
        name = message.name
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
    
    def handleInputMessage(self, n, message):
        if n in self.connections:
            self.messages.put(("input", self.connections[n], message.inp))
    
    def handleChatMessage(self, n, msg):#if n in self.connections:
            name = self.connections[n]
            message = name + ": " + msg.text
            print(message)
            self.broadcast(message, "chat")
        
    
    def error(self, n, errtype, description=""):
        self.serv.send(n, bytes(json.dumps(["error", errtype, description]), "utf-8"))
    
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



