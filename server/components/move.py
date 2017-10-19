

class Move:
    
    def __init__(self, slowness=1):
        self.direction = None
        self.moveCooldown = 0
        self.slowness = slowness
    
    def attach(self, obj, events):
        self.owner = obj
        self.updateEvent = events["update"]
        self.updateEvent.addListener(self.update)
        
    
    def move(self, direction):
        self.direction = direction
    
    def update(self):
        
        self.moveCooldown = max(self.moveCooldown-1, 0)
        
        
        neighbours = self.owner.getGround().getNeighbours()
        if self.direction in neighbours and self.moveCooldown <= 0:
            newPlace = neighbours[self.direction]
            
            if newPlace.accessible():
                self.owner.place(newPlace)
                self.moveCooldown = self.slowness
                newPlace.onEnter(self.owner)
            
            self.direction = None
    
    def remove(self):
        self.updateEvent.removeListener(self.update)
