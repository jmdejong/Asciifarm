import time

from . import gameserver
from . import world
from . import view
from . import utils
import os
import json

saveExt = ".save.json"


class Game:
    
    def __init__(self, socketType, worldData=None, loadDir=None, saveDir=None, saveInterval=1):
        
        self.server = gameserver.GameServer(self, socketType)
        
        self.world = world.World(worldData)
        self.load(loadDir)
        
        self.saveDir = saveDir
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
        
        if self.saveDir and not self.counter % self.saveInterval:
            self.save()
        
        self.counter += 1
    
    def save(self):
        try:
            os.mkdir(self.saveDir, 0o755)
        except FileExistsError:
            # This is the expected scenario.
            # The save function should just create the file if it doesn't exist
            # The only problem is when there is a file (not directory) with the same name, or a directory with the wrong permissions
            # These errors won;t be caught now and happen later
            pass
        for room in self.world.getActiveRooms():
            utils.writeFileSafe(os.path.join(self.saveDir, room + saveExt), json.dumps(self.world.getPreserved(room)))
            self.world.deactivateRoom(room)
            print("saved room:", room)
    
    def load(self, loadDir):
        try:
            fnames = os.listdir(loadDir)
        except FileNotFoundError:
            # Just continue, the game can and should also run without loading a save
            print("no saves loaded")
            return
        for fname in fnames:
            if fname.endswith(saveExt):
                room = fname[:-len(saveExt)]
                with open(os.path.join(loadDir, fname), 'r') as f:
                    data = json.load(f)
                    self.world.loadPreserved(room, data)
                    print("loaded save for:", room)
    
    def sendState(self):
        
        self.server.sendState(self.view)
        self.world.resetChangedCells()
        

