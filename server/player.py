
import playerent

class Player:
    
    def __init__(self, name, world):
        
        self.name = name
        self.world = world
        
        self.roomname = None
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
    
    def joinRoom(self, roomname, place=None):
        room = self.world.getRoom(roomname)
        if self.entity:
            self.leaveRoom()
        
        self.roomname = roomname
        pos = place or room.getEntrance()
        self.entity = playerent.Player(pos, room)
        self.entity.setController(self.controller)
        room.addObj(pos, self.entity)
    
    def getRoom(self):
        return self.world.getRoom(self.roomname)
    
    def getInventory(self):
        if self.entity:
            return self.entity.holding
        else:
            return None
    
    def control(self, action):
        self.controller["action"] = action
        #return self.controller
    
