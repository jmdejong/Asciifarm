
import playerent

class Player:
    
    def __init__(self, name):
        
        self.name = name
        
        self.room = None
        #self.pos = (0,0)
        
        self.entity = None
        
        self.data = {}
        
        self.controller = {}
    
    def updateData(self):
        if self.entity:
            pass
            #self.data = self.entity.toJSON
    
    def leaveRoom(self):
        self.entity.remove()
    
    def joinRoom(self, room, place=None):
        if self.entity:
            self.leaveRoom()
        self.room = room
        pos = place or room.getEntrance()
        self.entity = playerent.Player(pos, room)
        self.entity.setController(self.controller)
        room.addObj(pos, self.entity)
    
    def getRoom(self):
        return self.room
    
    def getInventory(self):
        if self.entity:
            return self.entity.holding
        else:
            return None
    
    def control(self, action):
        self.controller["action"] = action
        #return self.controller
    
