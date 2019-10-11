#! /usr/bin/python3


import json
import queue
import string
import threading


from . import view
from . import socketserver as server
from . import player
from . import controls

from asciifarm.common import messages

import re
import selectors


class GameServer:
    
    
    def __init__(self, sockets):
        
        self.servers = [server.Server(socket, self.newConnection, self.receive, self.close) for socket in sockets]
        
        self.connections = {}
        self.players = {}
        self.messages = queue.Queue()
    
    def start(self):
        selector = selectors.DefaultSelector()
        for serv in self.servers:
            serv.listen(selector)
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
    
    def newConnection(self, connection):
        pass
    
    def receive(self, connection, data):
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
            
            self.handleMessage(connection, message)
            
        except messages.InvalidMessageError as e:
            self.sendMessage(connection, e.toMessage())
        except json.JSONDecodeError:
            self.error(connection, "invalidmessage", "Invalid JSON")
        except Exception as e:
            print(type(e), e, data)
            self.error(connection, "invalidmessage", "An unknown error occured in handling the message")
    
    def handleMessage(self, connection, message):
        # I wish I had type overloading
        if isinstance(message, messages.NameMessage):
            self.handleNameMessage(connection, message)
        elif isinstance(message, messages.InputMessage):
            self.handleInputMessage(connection, message)
        elif isinstance(message, messages.ChatMessage):
            self.handleChatMessage(connection, message)
        else:
            self.error(connection, "invalidmessage", "unknown message '{}'".format(message.__class__))
    
    
    def handleNameMessage(self, connection, message):
        name = message.name
        serv, client = connection
        if name[0] == "~" and name[1:] != serv.getUsername(client):
            raise messages.InvalidNameError("tildenames are only available on unix sockets and when the rest of the name equals the username")
        if name in self.players:
            raise messages.InvalidNameError("another connection to this player already exists", "nametaken")
            return
        self.connections[connection] = name
        self.players[name] = connection
        self.messages.put(("join", name))
        print("new player: "+name)
        self.broadcast("{} has connected".format(name), "connect")
    
    def handleInputMessage(self, connection, message):
        if connection in self.connections:
            control = controls.controlFromJson(message.inp)
            self.messages.put(("input", self.connections[connection], control))
    
    def handleChatMessage(self, connection, msg):
            name = self.connections[connection]
            message = name + ": " + msg.text
            print(message)
            self.broadcast(message, "chat")
    
    def sendMessage(self, connection, message):
        serv, client = connection
        serv.send(client, message.to_json_bytes())
    
    def error(self, connection, errtype, description=""):
        self.sendMessage(connection, messages.ErrorMessage(errtype, description))
    
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



