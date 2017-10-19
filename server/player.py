
import playerent
import components
import event

class Player:
    
    def __init__(self, name, world):
        
        self.name = name
        self.world = world
        
        self.roomname = None
        
        self.entity = None
        
        self.data = {}
        self.inventory = components.Inventory(10)
        
    
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
        observable = event.Event()
        observable.addListener(self.onPlayerAction)
        self.entity = room.makeObject("player", components={
            "inventory": self.inventory,
            "move": components.Move(slowness=2),
            "controller": components.InputController(),
            "observable": observable
            })
        room.addObj(pos, self.entity)
    
    def getRoom(self):
        return self.roomname
    
    def onPlayerAction(self, action, *data):
        if action == "changeroom":
            room, pos = data
            self.joinRoom(room, pos)
    
    def getInventory(self):
        if self.entity:
            return self.entity.getComponent("inventory").getItems()
        else:
            return []
    
    def control(self, action):
        if not self.entity:
            return
        controller = self.entity.getComponent("controller")
        controller.control(action)
    
    def performAction(self, action, obj):
        if not self.entity:
            return
        self.entity.performAction(action, obj)
    
    def getInteractions(self):
        if not self.entity:
            return None
        controller = self.entity.getComponent("controller")
        return controller.getInteractions()
    
    def getGroundObjs(self):
        if not self.entity:
            return None
        objs = set(self.entity.getGround().getObjs())
        objs.discard(self.entity)
        return objs
    
