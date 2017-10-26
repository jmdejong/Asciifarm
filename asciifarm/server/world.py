from . import room
from . import player


# The World class is like the model in the MVC pattern (though the rest is not that clear)

class World:
    
    def __init__(self, data={"begin": None, "rooms": {}}):
        
        self.rooms = {}
        self.beginRoom = data["begin"]
        
        self.players = {}
        
        for roomname, roomdata in data["rooms"].items():
            self.makeRoom(roomname, roomdata)
    
    
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
            r = self.getBeginRoom()
        pl.joinRoom(r)
        return pl
    
    def makeRoom(self, name, data):
        ro = room.Room(name, data)
        self.rooms[name] = ro
        return ro
    
    def update(self):
        
        for r in self.rooms.values():
            r.update()
        
        for player in self.players:
            self.controlPlayer(player, None)
    
    def getPlayer(self, playername):
        return self.players[playername]
    
    def hasPlayer(self, playername):
        return playername in self.players
    
    def getRoom(self, roomname):
        return self.rooms.get(roomname)
    
    def getBeginRoom(self):
        return self.beginRoom
    
    def controlPlayer(self, playername, action):
        self.players[playername].control(action)
    
    def removePlayer(self, name):
        if name not in self.players:
            return
        pl = self.players[name]
        pl.leaveRoom()
    
    def resetChangedCells(self):
        for room in self.rooms.values():
            room.resetChangedCells()
