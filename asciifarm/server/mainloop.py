import time

from . import gameserver
from . import world
from . import view


class Game:
    
    def __init__(self, socketType, worldData):
        
        self.server = gameserver.GameServer(self, socketType)
        
        self.world = world.World(worldData)
        
        self.view = view.View(self.world)
    
        
    def start(self, address):
        
        self.server.start(address)
        
        self.game_loop()
    
    
    def game_loop(self):
        
        keepRunning = True
        while keepRunning:
            
            self.update()
            self.sendState()
            time.sleep(0.1)
    
    def update(self):
        
        messages = self.server.readMessages()
        
        for msg in messages:
            t = msg[0]
            name = msg[1]
            if t == "join":
                if not self.world.hasPlayer(name):
                    self.world.createPlayer(name)
                self.world.playerJoin(name)
            elif t == "leave":
                self.world.removePlayer(name)
            elif t == "input":
                self.world.controlPlayer(name, msg[2])
            
        
        self.world.update()
        
    
    def sendState(self):
        
        self.server.sendState(self.view)
        self.world.resetChangedCells()
        

