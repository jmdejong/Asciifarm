#! /usr/bin/python3



import json
import server
import view
import player
import queue


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
                        self.serv.send(n, bytes(json.dumps(["error", "nametaken"]), "utf-8"))
                    else:
                        self.connections[n] = name
                        self.players[name] = n
                        self.messages.put(("join", name))
                        print("new player: "+name)
                elif msgType == "input":
                    if n in self.connections:
                        self.messages.put(("input", self.connections[n], msg[1]))
        except Exception as e:
            self.serv.send(n, bytes(json.dumps(["error", "invalidmessage"]), "utf-8"))
    
    
    def close(self, connection):
        if connection in self.connections:
            name = self.connections[connection]
            del self.connections[connection]
            del self.players[name]
            self.messages.put(("leave", name))
            print("player "+name+" left")
        
    
    def readMessages(self):
        m = []
        while not self.messages.empty():
            m.append(self.messages.get())
        return m



