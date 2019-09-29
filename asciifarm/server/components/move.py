
from .component import Component


class MoveData(Component):
    
    def __init__(self, slowness=1):
        self.direction = None
        self.slowness = slowness
        self.moveReady = 0
    
    def canMove(self, obj, direction):
        neighbours = obj.getGround().getNeighbours()
        return direction in neighbours and neighbours[direction].accessible()

class Move(Component):
    
    def __init__(self, slowness=1):
        self.direction = None
        self.slowness = slowness
        self.moveReady = 0
    
    def attach(self, obj):
        self.owner = obj
        obj.addListener("roomjoin", self.roomJoin)
    
    def roomJoin(self, o, roomData, stamp):
        self.roomData = roomData
        
    
    def move(self, direction):
        self.direction = direction
        
    def canMove(self, direction):
        neighbours = self.owner.getGround().getNeighbours()
        return direction in neighbours and neighbours[direction].accessible()
    
    def doMove(self):
        neighbours = self.owner.getGround().getNeighbours()
        if self.canMove(self.direction) and self.roomData.getStamp() > self.moveReady:
            newPlace = neighbours[self.direction]
            
            if newPlace.accessible():
                self.owner.place(newPlace)
                self.moveReady = self.roomData.getStamp() + self.slowness
                self.owner.trigger("move")
            
        self.direction = None
    
    def toJSON(self):
        return {"slowness": self.slowness}

