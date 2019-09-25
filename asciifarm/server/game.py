import time
import os
import json

from . import gameserver
from . import world
from . import view
from asciifarm.common import utils
from . import roomloader
from . import playerloader
from . import worldloader

saveExt = ".save.json"


class Game:
    
    def __init__(self, socketType, address, worldFile=None, saveDir=None, saveInterval=1):

        self.server = gameserver.GameServer(socketType, address)
        
        worldLoader = worldloader.WorldLoader(saveDir)
        roomLoader = roomloader.RoomLoader(worldFile, os.path.join(saveDir, "rooms"))
        playerLoader = playerloader.PlayerLoader(os.path.join(saveDir, "players"))
        self.world = world.World(worldLoader, roomLoader, playerLoader)
        
        self.saveInterval = saveInterval
        
        self.view = view.View(self.world)
        
        self.counter = 0
    
        
    def start(self):
        
        self.server.start()
        
        try:
            self.game_loop()
        except KeyboardInterrupt:
            print("\n^C caught, saving")
            self.world.save()
    
    
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
        
        if (self.counter % self.saveInterval) == 0:
            self.world.save()
            self.world.checkRoomActivity(599)
        
        self.counter += 1
    
    def sendState(self):
        
        self.server.sendState(self.view)
        self.world.resetChangedCells()
    
        
    
        

