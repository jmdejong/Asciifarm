
from .component import Component

class Move(Component):
    
    def __init__(self, slowness=1):
        self.direction = None
        self.slowness = slowness
        self.canMove = False
    
    def attach(self, obj):
        self.owner = obj
        obj.addListener("roomjoin", self.roomJoin)
    
    def roomJoin(self, o, roomData, stamp):
        self.roomData = roomData
        self.moveEvent = roomData.getEvent("move")
        self.canMove = True
        
    
    def move(self, direction):
        self.direction = direction
        self.moveEvent.addListener(self.doMove)
        
    def canMove(self, direction):
        neighbours = self.owner.getGround().getNeighbours()
        return direction in neighbours and neighbours[direction].accessible()
    
    def doMove(self):
        neighbours = self.owner.getGround().getNeighbours()
        if self.direction in neighbours and self.canMove:
            newPlace = neighbours[self.direction]
            
            if newPlace.accessible():
                self.owner.place(newPlace)
                self.canMove = False
                self.roomData.setAlarm(self.roomData.getStamp() + self.slowness, self.makeReady)
                self.owner.trigger("move")
            
        self.direction = None
        self.moveEvent.removeListener(self.doMove)
    
    def makeReady(self):
        self.canMove = True
    
    def remove(self):
        self.moveEvent.removeListener(self.doMove)
    
    def toJSON(self):
        return {"slowness": self.slowness}

