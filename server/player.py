
import playerent

class Player:
    
    def __init__(self, name, world):
        
        self.name = name
        self.world = world
        
        self.roomname = None
        
        self.entity = None
        
        self.data = {}
        
        self.controller = {}
        
    
    def updateData(self):
        if self.entity:
            pass
    
    def leaveRoom(self):
        self.entity.remove()
    
    def joinRoom(self, roomname, place=None):
        room = self.world.getRoom(roomname)
        if not room:
            raise Exception("Invalid Room")
        
        if self.entity:
            self.leaveRoom()
        
        self.roomname = roomname
        pos = place or room.getEntrance()
        self.entity = playerent.Player(room)
        self.entity.setController(self.controller)
        self.entity.getEvent().addListener(self.onPlayerAction)
        room.addObj(pos, self.entity)
    
    def getRoom(self):
        return self.roomname
    
    def onPlayerAction(self, action, *data):
        if action == "changeroom":
            room, pos = data
            self.joinRoom(room, pos)
    
    def getInventory(self):
        if self.entity:
            return self.entity.holding
        else:
            return None
    
    def control(self, action):
        if action in {"north", "south", "east", "west"}:
            self.controller["action"] = action
        else:
            self.controller["action"] = None
        
        for interaction, obj in self.getInteractions():
            if action == interaction:
                self.performAction(action, obj)
    
    def performAction(self, action, obj):
        if not self.entity:
            return
        self.entity.performAction(action, obj)
    
    def getInteractions(self):
        if not self.entity:
            return None
        objs = set(self.entity.getNearObjects())
        objs.discard(self.entity)
        for item in self.entity.getInventory():
            objs.add(item)
        #objs |= {self.entity.holding}
        interactions = set()
        for obj in objs:
            #print("a ",obj.getInteractions())
            for action in obj.getInteractions():
                if action in self.entity.getActions():
                    #print(action)
                    interactions.add((action, obj))
        return interactions
    
    def getGroundObjs(self):
        if not self.entity:
            return None
        objs = set(self.entity.getGround().getObjs())
        objs.discard(self.entity)
        return objs
    
