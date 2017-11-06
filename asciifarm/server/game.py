import time

from . import gameserver
from . import world
from . import view
import pickle
import os


class Game:
    
    def __init__(self, socketType, worldData=None, worldSave=None, saveAs=None, saveInterval=1):
        
        self.server = gameserver.GameServer(self, socketType)
        
        if worldSave:
            with open(worldSave, "rb") as f:
                self.world = pickle.load(f)
        elif worldData:
            self.world = world.World(worldData)
        
        self.saveAs = saveAs
        self.saveInterval = saveInterval
        
        self.view = view.View(self.world)
        
        self.counter = 0
    
        
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
        
        if self.saveAs and not self.counter % self.saveInterval:
            tempName = self.saveas+".tmp"
            with open(tempName, "wb") as f:
                pickle.dump(self.world, f, 0)
            os.rename(tempName, self.saveAs)
        
        self.counter += 1
        
    
    def sendState(self):
        
        self.server.sendState(self.view)
        self.world.resetChangedCells()
        

