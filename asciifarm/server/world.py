from . import room
from . import player


# The World class is like the model in the MVC pattern (though the rest is not that clear)

class World:
    
    def __init__(self, worldLoader, roomLoader, playerLoader):
        
        self.rooms = {}
        
        self.players = {}
        
        self.activeRooms = {}
        
        self.worldLoader = worldLoader
        self.roomLoader = roomLoader
        self.playerLoader = playerLoader
        
        self.stepStamp = 0 # like a timestamp but with the number of ticks instead of the time
        
        data = self.worldLoader.load()
        if data:
            self.stepStamp = data["steps"]
    
    
    def createPlayer(self, name, data=None):
        
        if self.hasPlayer(name):
            raise Exception("Can not make new player with the name of an existing player")
        pl = player.Player(name, self)
        self.playerLoader.save(pl)
        return pl
    
    def playerJoin(self, name):
        pl = self.activatePlayer(name)
        r = pl.getRoom()
        pl.joinRoom(r)
        self.players[name] = pl
        return pl
    
    def update(self):
        
        for r in list(self.activeRooms.values()):
            r.update(self.stepStamp)
        
        self.stepStamp += 1
    
    def getPlayer(self, name):
        return self.players.get(name)
    
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
        for player in self.players.values():
            if player.getRoom() == name:
                return
        
        self.saveRoom(name)
        self.activeRooms.pop(name, None)
    
    def activatePlayer(self, name):
        if name in self.players:
            return self.players[name]
        player = self.playerLoader.load(name, self)
        self.players[name] = player
        return player
    
    def deactivatePlayer(self, name):
        self.savePlayer(name)
        pl = self.players.pop(name, None)
        if pl:
            pl.leaveRoom()
    
    def getActiveRooms(self):
        return list(self.activeRooms.keys())
    
    def getActivePlayers(self):
        return list(self.players.keys())
    
    def controlPlayer(self, playername, action):
        self.getPlayer(playername).control(action)
    
    def removePlayer(self, name):
        if name not in self.players:
            return
        self.deactivatePlayer(name)
    
    def resetChangedCells(self):
        for room in self.rooms.values():
            room.resetChangedCells()
    
    def getStepStamp(self):
        return self.stepStamp
    
    def saveRoom(self, name):
        self.roomLoader.save(self.rooms[name])
        
    def savePlayer(self, name):
        self.playerLoader.save(self.getPlayer(name))
    
    def saveWorld(self):
        self.worldLoader.save(self)
    
    def save(self):
        for room in self.getActiveRooms():
            self.saveRoom(room)
        for player in self.getActivePlayers():
            self.savePlayer(player)
        self.saveWorld()
    
    def getDefaultRoom(self):
        return self.getRoom(self.roomLoader.defaultRoomName())
        

