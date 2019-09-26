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
import selectors


class GameServer:
    
    
    def __init__(self, socketType, address):
        
        self.serv = server.Server(socketType, address, self.newConnection, self.receive, self.close)
        
        self.connections = {}
        self.players = {}
        self.messages = queue.Queue()
    
    def start(self):
        selector = selectors.DefaultSelector()
        self.serv.listen(selector)
        self.listener = threading.Thread(target=self.listen, daemon=True, args=(selector,))
        self.listener.start()
    
    def listen(self, selector):
        
        while True:
            events = selector.select()
            for key, mask in events:
                sock = key.fileobj
                callback = key.data
                callback(sock, selector)
    
    def sendState(self, view):
        
        for connection, name in list(self.connections.items()):
            data = view.playerView(name)
            if data is None:
                continue
            self.sendMessage(connection, messages.WorldMessage(data))
    
    def newConnection(self, n):
        pass
    
    def receive(self, n, data):
        try:
            data = json.loads(data.decode('utf-8'))
            if not isinstance(data, list) or len(data) != 2:
                raise messages.InvalidMessageError("Message must be a json list of length 2")
            msg = data
            msgType = msg[0]
            if not isinstance(msgType, str):
                raise messages.InvalidMessageError("Message type must be a string")
            msgClass = messages.messages.get(msgType)
            if msgClass is None:
                raise messages.InvalidMessageError("Unknown message type '{}'".format(msgType))
            message = msgClass.from_json(msg)
            
            self.handleMessage(n, message)
            
        except messages.InvalidMessageError as e:
            self.sendMessage(n, e.toMessage)
        except json.JSONDecodeError:
            self.error(n, "invalidmessage", "Invalid JSON")
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
            raise messages.InvalidNameError("tildenames are only available on unix sockets and when the rest of the name equals the username")
        if name in self.players:
            raise messages.InvalidNameError("another connection to this player already exists", "nametaken")
            return
        self.connections[n] = name
        self.players[name] = n
        self.messages.put(("join", name))
        print("new player: "+name)
        self.broadcast("{} has connected".format(name), "connect")
    
    def handleInputMessage(self, n, message):
        if n in self.connections:
            self.messages.put(("input", self.connections[n], message.inp))
    
    def handleChatMessage(self, n, msg):
            name = self.connections[n]
            message = name + ": " + msg.text
            print(message)
            self.broadcast(message, "chat")
    
    def sendMessage(self, n, message):
        self.serv.send(n, message.to_json_bytes())
    
    def error(self, n, errtype, description=""):
        self.sendMessage(n, messages.ErrorMessage(errtype, description))
    
    def close(self, connection):
        if connection in self.connections:
            name = self.connections[connection]
            del self.connections[connection]
            del self.players[name]
            self.messages.put(("leave", name))
            print("player "+name+" left")
            self.broadcast("{} has disconnected".format(name), "connect")
    
    def broadcast(self, text, type="server"):
        message = messages.MessageMessage(text, type)
        for connection in self.connections:
            self.sendMessage(connection, message)
        
    
    def readMessages(self):
        m = []
        while not self.messages.empty():
            try:
                message = self.messages.get_nowait()
            except queue.Empty:
                return m
            m.append(message)
        return m



