from . import room
from . import player


# The World class is like the model in the MVC pattern (though the rest is not that clear)

class World:
    
    def __init__(self, roomLoader, playerLoader):
        
        self.rooms = {}
        self.beginRoom = None
        
        self.players = {}
        
        self.activeRooms = {}
        self.activePlayers = {}
        
        self.roomLoader = roomLoader
        self.playerLoader = playerLoader
        
        self.stepStamp = 0 # like a timestamp but with the number of ticks instead of the time
    
    
    def createPlayer(self, name, data=None):
        
        if self.hasPlayer(name):
            raise Exception("Can not make new player with the name of an existing player")
        pl = player.Player(name, self)
        self.players[name] = pl
        self.playerLoader.save(pl)
        return pl
    
    def playerJoin(self, name):
        pl = self.getPlayer(name)
        r = pl.getRoom()
        if not r:
            r = self.beginRoom
        pl.joinRoom(r)
        self.players[name] = pl
        self.activePlayers[name] = pl
        return pl
    
    def update(self):
        
        for r in list(self.activeRooms.values()):
            r.update(self.stepStamp)
        
        for player in self.players:
            self.controlPlayer(player, None)
        
        self.stepStamp += 1
    
    def getPlayer(self, name):
        if name in self.players:
            return self.players[name]
        return self.playerLoader.load(name, self)
    
    def hasPlayer(self, name):
        return name in self.players or self.playerLoader.exists(name)
    
    def getRoom(self, name):
        if name not in self.rooms:
            room = self.roomLoader.load(name)
            if room:
                self.rooms[name] = room
        return self.rooms.get(name, None)
    
    def activateRoom(self, name):
        self.activeRooms[name] = self.getRoom(name)
        self.activeRooms[name].update(self.stepStamp)
    
    def deactivateRoom(self, name):
        
        # only deactivate a room when it's empty
        for player in self.activePlayers.values():
            if player.getRoom() == name:
                return
        
        self.activeRooms.pop(name, None)
        self.saveRoom(name)
    
    def deactivatePlayer(self, name):
        self.activePlayers.pop(name, None)
        self.savePlayer(name)
    
    def getActiveRooms(self):
        return list(self.activeRooms.keys())
    
    def getActivePlayers(self):
        return list(self.activePlayers.keys())
    
    def controlPlayer(self, playername, action):
        self.getPlayer(playername).control(action)
    
    def removePlayer(self, name):
        if name not in self.players:
            return
        pl = self.players[name]
        pl.leaveRoom()
        self.deactivatePlayer(name)
    
    def resetChangedCells(self):
        for room in self.rooms.values():
            room.resetChangedCells()
    
    def saveRoom(self, name):
        self.roomLoader.save(self.rooms[name])
        
    def savePlayer(self, name):
        self.playerLoader.save(self.players[name])
    
    def save(self):
        for room in self.getActiveRooms():
            self.saveRoom(room)
        for player in self.getActivePlayers():
            self.savePlayer(player)
        

