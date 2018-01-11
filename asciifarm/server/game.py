import time

from . import gameserver
from . import world
from . import view
from .worldtemplate import WorldTemplate
from asciifarm.common import utils
import os
import json

saveExt = ".save.json"


class Game:
    
    def __init__(self, socketType, worldData={"begin": None, "rooms": {}}, loadDir=None, saveDir=None, saveInterval=1):
        
        self.server = gameserver.GameServer(self, socketType)
        
        
        template = WorldTemplate()
        template.addPrefabs(worldData["rooms"])
        self.world = world.World(template, worldData["begin"])
        self.load(loadDir)
        
        self.saveDir = saveDir
        self.playerSaveDir = os.path.join(self.saveDir, "players")
        self.roomSaveDir = os.path.join(self.saveDir, "rooms")
        self.makeSaveDirs()
        self.saveInterval = saveInterval
        
        self.lastActivePlayers = set()
        
        self.view = view.View(self.world)
        
        self.counter = 0
    
        
    def start(self, address):
        
        self.server.start(address)
        
        try:
            self.game_loop()
        except KeyboardInterrupt:
            print("\n^C caught, saving")
            self.save()
    
    
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
                self.lastActivePlayers.add(name)
            elif t == "leave":
                self.world.removePlayer(name)
            elif t == "input":
                self.world.controlPlayer(name, msg[2])
            
        self.world.update()
        
        if self.saveDir and not self.counter % self.saveInterval:
            self.save()
        
        self.counter += 1
    
    def sendState(self):
        
        self.server.sendState(self.view)
        self.world.resetChangedCells()
    
    def makeSaveDirs(self):
        try:
            os.mkdir(self.saveDir, 0o755)
        except FileExistsError:
            # This is the expected scenario.
            # The save function should just create the file if it doesn't exist
            # The only problem is when there is a file (not directory) with the same name, or a directory with the wrong permissions
            # These errors won't be caught now and happen later
            pass
        try:
            os.mkdir(self.playerSaveDir, 0o700)
        except FileExistsError:
            # same here
            pass
        try:
            os.mkdir(self.roomSaveDir, 0o755)
        except FileExistsError:
            # same again
            pass
    
    def save(self):
        
        playerDir = self.playerSaveDir
        activePlayers = set(self.world.getActivePlayers())
        for player in activePlayers.union(self.lastActivePlayers):
            utils.writeFileSafe(os.path.join(playerDir, player + saveExt), json.dumps(self.world.savePlayer(player)))
        self.lastActivePlayers = activePlayers
        
        roomDir = self.roomSaveDir
        for room in self.world.getActiveRooms():
            utils.writeFileSafe(os.path.join(roomDir, room + saveExt), json.dumps(self.world.getPreserved(room)))
            self.world.deactivateRoom(room)
        
    
    def load(self, loadDir):
        
        roomDir = os.path.join(loadDir, "rooms")
        try:
            fnames = os.listdir(roomDir)
        except FileNotFoundError:
            print("no room saves loaded")
            return
        for fname in fnames:
            if fname.endswith(saveExt):
                room = fname[:-len(saveExt)]
                with open(os.path.join(roomDir, fname), 'r') as f:
                    data = json.load(f)
                    self.world.loadPreserved(room, data)
                    print("loaded saved room:", room)
        
        playerDir = os.path.join(loadDir, "players")
        try:
            fnames = os.listdir(playerDir)
        except FileNotFoundError:
            print("no player saves loaded")
            return
        for fname in fnames:
            if fname.endswith(saveExt):
                player = fname[:-len(saveExt)]
                with open(os.path.join(playerDir, fname), 'r') as f:
                    data = json.load(f)
                    self.world.loadPlayer(player, data)
                    print("loaded saved player:", player)
        

