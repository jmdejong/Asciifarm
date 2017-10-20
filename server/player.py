
import components
import event
from components.inventory import Inventory
from components.inputcontroller import InputController
from components.move import Move
from components.fighter import Fighter
from components.faction import GOOD, EVIL, NEUTRAL

class Player:
    
    def __init__(self, name, world):
        
        self.name = name
        self.world = world
        
        self.roomname = None
        
        self.entity = None
        
        self.data = {}
        self.inventory = Inventory(10)
        
    
    def leaveRoom(self):
        if self.entity:
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
        self.entity = room.makeEntity(
            sprite = "player",
            solid = False,
            height = 2,
            name = '~' + self.name,
            components={
                "inventory": self.inventory,
                "move": Move(slowness=2),
                "controller": InputController(),
                "observable": observable,
                "fighter": Fighter(10000, 5, slowness=2),
                "alignment": GOOD
                })
        room.addObj(pos, self.entity)
    
    def getRoom(self):
        return self.roomname
    
    def onPlayerAction(self, action, *data):
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
        
        if action == "die":
            obj = data[0]
            print("{} got killed by {}".format(self.name, obj.getName()))
            self.entity = None
        
    
    def control(self, action):
        if not self.entity:
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
    
