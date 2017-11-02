import time

from . import gameserver
from . import world
from . import view
import pickle
import os


class Game:
    
    def __init__(self, socketType, worldData):
        
        self.server = gameserver.GameServer(self, socketType)
        
        #self.world = world.World(worldData)
        with open("savegame", "rb") as f:
            self.world = pickle.load(f)
        
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
        
        if not self.counter % 5:
            with open(".savegame.tmp", "wb") as f:
                pickle.dump(self.world, f, 0)
                print("saved", self.counter)
            os.rename(".savegame.tmp", "savegame")
        
        self.counter += 1
        
    
    def sendState(self):
        
        self.server.sendState(self.view)
        self.world.resetChangedCells()
        

