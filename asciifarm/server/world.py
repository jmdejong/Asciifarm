from . import room
from . import player


# The World class is like the model in the MVC pattern (though the rest is not that clear)

class World:
    
    def __init__(self, data={"begin": None, "rooms": {}}):
        
        self.rooms = {}
        self.beginRoom = data["begin"]
        
        self.players = {}
        
        self.activeRooms = {}
        self.activePlayers = {}
        
        for roomname, roomdata in data["rooms"].items():
            self.makeRoom(roomname, roomdata)
        
        self.stepStamp = 0 # like a timestamp but with the number of ticks instead of the time
    
    
    def createPlayer(self, name, data=None):
        
        if name in self.players:
            raise Exception("Can not make new player with the name of an existing player")
        pl = player.Player(name, self)
        self.players[name] = pl
        return pl
    
    def playerJoin(self, name):
        pl = self.players[name]
        r = pl.getRoom()
        if not r:
            r = self.beginRoom
        pl.joinRoom(r)
        self.activePlayers[name] = pl
        return pl
    
    def makeRoom(self, name, data):
        ro = room.Room(name, data)
        self.rooms[name] = ro
        return ro
    
    def update(self):
        
        for r in list(self.activeRooms.values()):
            r.update(self.stepStamp)
        
        for player in self.players:
            self.controlPlayer(player, None)
        
        self.stepStamp += 1
    
    def getPlayer(self, playername):
        return self.players[playername]
    
    def hasPlayer(self, playername):
        return playername in self.players
    
    def getRoom(self, roomname):
        return self.rooms.get(roomname)
    
    def activateRoom(self, name):
        self.activeRooms[name] = self.rooms[name]
        self.activeRooms[name].update(self.stepStamp)
    
    def deactivateRoom(self, name):
        
        # only deactivate a room when it's empty
        for player in self.players.values():
            if player.isActive() and player.getRoom() == name:
                return
        
        self.activeRooms.pop(name, None)
    
    def getActiveRooms(self):
        return list(self.activeRooms.keys())
    
    def getActivePlayers(self):
        return list(self.activePlayers.keys())
    
    def getPreserved(self, roomName):
        return self.getRoom(roomName).getPreserved()
    
    def loadPreserved(self, roomName, data):
        self.getRoom(roomName).loadPreserved(data)
    
    def controlPlayer(self, playername, action):
        self.players[playername].control(action)
    
    def removePlayer(self, name):
        if name not in self.players:
            return
        pl = self.players[name]
        pl.leaveRoom()
        self.activePlayers.pop(name, None)
    
    def resetChangedCells(self):
        for room in self.rooms.values():
            room.resetChangedCells()
    
    def savePlayer(self, name):
        return self.players[name].toJSON()
    
    def loadPlayer(self, name, data):
        self.players[name] = player.Player.fromJSON(data, self)
