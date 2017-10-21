
from components.inventory import Inventory
from components.inputcontroller import InputController
from components.move import Move
from components.fighter import Fighter
from components.healing import Healing
from components.alignment import Alignment
import faction

class Player:
    
    def __init__(self, name, world):
        
        self.name = name
        self.world = world
        
        self.roomname = None
        
        self.entity = None
        
        self.data = {}
        # todo: ensure that items have correct roomData when inventory changes room
        self.inventory = Inventory(10)
        self.health = None
        self.maxHealth = 100
        
        self.resetView = True
        
    
    def leaveRoom(self):
        if self.entity:
            self.health = self.getHealth()
            self.entity.remove()
            self.entity = None
    
    def joinRoom(self, roomname, place=None):
        room = self.world.getRoom(roomname)
        if not room:
            raise Exception("Invalid Room")
        
        if self.entity:
            self.leaveRoom()
        
        pos = place or room.getEntrance()
        self.entity = room.makeEntity(
            sprite = "player",
            solid = False,
            height = 2,
            name = '~' + self.name,
            components={
                "inventory": self.inventory,
                "move": Move(slowness=2),
                "controller": InputController(),
                "fighter": Fighter(self.maxHealth, 5, slowness=2, health=self.health or self.maxHealth),
                "alignment": Alignment(faction.GOOD),
                "heal": Healing(interval=25)
                })
        
        self.entity.addListener(self.onPlayerAction)
        room.addObj(pos, self.entity)
        
        self.roomname = roomname
        self.place = pos
        
        self.resetView = True
    
    def getRoom(self):
        return self.roomname
    
    def onPlayerAction(self, o, action, *data):
        if action == "changeroom":
            room, pos = data
            self.joinRoom(room, pos)
        
        if action == "attack":
            obj, damage = data
            print("{} attacks {} for {} damage".format(self.name, obj.getName(), damage))
        
        if action == "kill":
            obj = data[0]
            print("{} kills {}".format(self.name, obj.getName()))
        
        if action == "damage":
            obj, damage = data
            print("{} got {} damage from {}".format(self.name, damage, obj.getName()))
        
        if action == "heal":
            obj, health = data
            if obj:
                print("{} got {} health from {}".format(self.name, health, obj.getName()))
        
        if action == "die":
            obj = data[0]
            print("{} got killed by {}".format(self.name, obj.getName()))
            self.entity = None
            self.roomname = None
            self.place = None
        
    
    def control(self, action):
        if not self.entity or not (isinstance(action, list) or isinstance(action, tuple)) or len(action) < 1:
            return
        controller = self.entity.getComponent("controller")
        controller.addAction(action)
    
    def getHealth(self):
        if self.entity:
            return self.entity.getComponent("fighter").getHealth()
        else:
            return None
    
    def getInventory(self):
        if self.entity:
            return self.inventory.getItems()
        else:
            return []
    
    def getInteractions(self):
        if not self.entity:
            return []
        controller = self.entity.getComponent("controller")
        return controller.getInteractions()
    
    def getGroundObjs(self):
        if not self.entity:
            return []
        objs = set(self.entity.getGround().getObjs())
        objs.discard(self.entity)
        return objs
    
    def shouldResetView(self):
        return self.resetView
    
    def viewResetDone(self):
        self.resetView = False
