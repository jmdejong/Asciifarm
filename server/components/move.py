
import timeout

class Move:
    
    def __init__(self, slowness=1):
        self.direction = None
        self.slowness = slowness
    
    def attach(self, obj, events):
        self.owner = obj
        self.moveEvent = events["move"]
        self.timeout = timeout.Timeout(events["update"], self.slowness)
        
    
    def move(self, direction):
        self.direction = direction
        self.moveEvent.addListener(self.doMove)
        
    def canMove(self, direction):
        neighbours = self.owner.getGround().getNeighbours()
        return direction in neighbours and neighbours[direction].accessible()
    
    def doMove(self):
        neighbours = self.owner.getGround().getNeighbours()
        if self.direction in neighbours and self.timeout.isReady():
            newPlace = neighbours[self.direction]
            
            if newPlace.accessible():
                self.owner.place(newPlace)
                self.timeout.timeout()
                newPlace.onEnter(self.owner)
            
        self.direction = None
        self.moveEvent.removeListener(self.doMove)
        
    
    def remove(self):
        self.moveEvent.removeListener(self.doMove)
        self.timeout.remove()

