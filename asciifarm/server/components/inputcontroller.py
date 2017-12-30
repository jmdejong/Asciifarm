
from .component import Component

class InputController(Component):
    
    def __init__(self):
        self.actions = [] #queue.Queue()
        
        self.handlers = {
            "move": self.do_move,
            "take": self.do_take,
            "drop": self.do_drop,
            "use": self.do_use,
            "interact": self.do_interact,
            "attack": self.do_attack,
            "say": self.do_say
        }
            
    
    def attach(self, obj):
        self.owner = obj
        
        for dep in {"inventory", "move", "fighter", "alignment"}:
            if not obj.getComponent(dep):
                # todo: better exception
                raise Exception("InputController needs object with " + dep + " component")
            
            setattr(self, dep, obj.getComponent(dep))
        
        obj.addListener("roomjoin", self.roomJoin)
    
    def roomJoin(self, o, roomData):
        self.roomData = roomData
        self.controlEvent = roomData.getEvent("control")
        self.controlEvent.addListener(self.control)
    
    def addAction(self, action):
        self.actions.append(action)
    
    
    def control(self):
        actions = self.actions
        self.actions = []
        for action in actions:
            self.executeAction(action)
        #while not self.actions.empty():
            #action = self.actions.get()
            #self.executeAction(action)
    
    def executeAction(self, action):
        kind = action[0]
        
        if kind in self.handlers:
            try:
                self.handlers[kind](*action[1:])
            except TypeError:
                # invalid command.
                # We can't notify the client from here
                # The server can't really do anything with a notification
                pass
    
    def do_move(self, direction):
            self.move.move(direction)
    
    def do_take(self, rank=None):
        objects = self.owner.getNearObjects()
        if rank != None:
            if rank not in range(len(objects)):
                return
            objects = [objects[rank]]
        for obj in objects:
            if obj.getComponent("item") != None and self.inventory.canAdd(obj):
                self.owner.trigger("take", obj)
                obj.remove()
                break
    
    def do_drop(self, rank=0):
        items = self.inventory.getItems()
        if rank not in range(len(items)):
            return
        obj = items[rank]
        self.inventory.drop(obj)
        obj.construct(self.roomData, preserve=True)
        obj.place(self.owner.getGround())
        
    def do_use(self, rank=0):
        items = self.inventory.getItems()
        if rank not in range(len(items)):
            return
        obj = items[rank]
        obj.getComponent("item").use(self.owner)
    
    def do_interact(self, rank=None):
        nearPlaces = self.owner.getGround().getNeighbours()
        objects = self.owner.getNearObjects()
        if rank != None:
            if rank not in range(len(objects)):
                return
            objects = [objects[rank]]
        for obj in objects:
            if obj.getComponent("interact") != None:
                obj.getComponent("interact").interact(self.owner)
                break
    
    def do_attack(self, direction=None):
        nearPlaces = self.owner.getGround().getNeighbours()
        if direction in nearPlaces:
            objs = nearPlaces[direction].getObjs()
        else:
            objs = self.owner.getNearObjects()
        for obj in objs:
            if obj.getComponent("fighter") != None and self.alignment.isEnemy(obj):
                self.fighter.attack(obj)
                break
    
    def do_say(self, text):
        self.roomData.getEvent("sound").trigger(self.owner, text)
    
    def getInteractions(self):
        return []
    
    def remove(self):
        self.controlEvent.removeListener(self.control)


