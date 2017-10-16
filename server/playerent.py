
from placable import GameObject
import event

class Player(GameObject):
    
    char = 'player'
    size = 2
    direction = None
    attributes = {}
    slowness = 2
    
    def __init__(self, room, pos, name=None):
        self.controller = {}
        self.room = room
        self.name = name or str(id(self))
        #self.char = self.name[0]
        x, y = pos
        self.x = x
        self.y = y
        #self.ground = None
        self.place((x, y))
        self.holding = None
        self.moveCooldown = 0
        #self.direction = random.choice(["north", "south", "east", "west"])
        room.addUpdateListener(self.update, self)
        self.event = event.Event()
    
    def setController(self, controller):
        self.controller = controller
    
    def place(self, pos):
        x, y = pos
        self.room.removeObj((self.x, self.y), self)
        self.room.addObj((x, y), self)
        #self.ground = self.room.get(x, y)
        self.x = x
        self.y = y
            
    
    def update(self):
        self.moveCooldown = max(self.moveCooldown-1, 0)
        
        if "action" in self.controller:
            action = self.controller["action"]
            
            if action in {"north", "east", "south", "west"} and self.moveCooldown <= 0:
                direction = action
                dx = (direction == "east") - (direction == "west")
                dy = (direction == "south") - (direction == "north")
                
                newx = self.x + dx
                newy = self.y + dy
                
                if self.room.accessible((newx, newy)):
                    self.place((newx, newy))
                    self.moveCooldown = self.slowness
                    self.room.onEnter((self.x, self.y), self)
            
            
            if action == "drop" and self.holding:
                self.room.addObj((self.x, self.y), self.holding)
                self.holding = None
            
            if action == "take" and not self.holding:
                #place = self.field.get(self.x, self.y)
                for obj in self.room.getObjs((self.x, self.y)):
                    if "takable" in obj.attributes:
                        self.room.removeObj((self.x, self.y), obj)
                        self.holding = obj
                        break
            
    
    def remove(self):
        #self.game.removePlayer(self.name)
        self.room.removeObj((self.x, self.y), self)
        self.room.removeUpdateListener(self)
    
    def getEvent(self):
        return self.event
    
    def getPos(self):
        return (self.x, self.y)

