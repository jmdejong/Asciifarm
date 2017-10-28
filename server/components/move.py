
import timeout

class Move:
    
    def __init__(self, slowness=1):
        self.direction = None
        self.slowness = slowness
        self.canMove = False
        self.timeout = None
    
    def attach(self, obj, roomData):
        self.owner = obj
        self.moveEvent = roomData.getEvent("move")
        self.updateEvent = roomData.getEvent("update")
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
                self.timeout = timeout.Timeout(self.updateEvent, self.slowness, self.makeReady)
                #newPlace.onEnter(self.owner)
                self.owner.trigger("move")
            
        self.direction = None
        self.moveEvent.removeListener(self.doMove)
    
    def makeReady(self, to):
        self.canMove = True
        self.timeout = None
    
    def remove(self):
        self.moveEvent.removeListener(self.doMove)
        self.timeout and self.timeout.remove()

