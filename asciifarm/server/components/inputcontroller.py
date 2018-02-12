
from .component import Component

class InputController(Component):
    
    def __init__(self):
        self.actions = [] #queue.Queue()
        
        self.handlers = {
            "move": self.do_move,
            "take": self.do_take,
            "drop": self.do_drop,
            "use": self.do_use,
            "unequip": self.do_unequip,
            "interact": self.do_interact,
            "attack": self.do_attack,
            "say": self.do_say
        }
        self.hasInteracted = False
        self.hasAttacked = False
            
    
    def attach(self, obj):
        self.owner = obj
        
        for dep in {"inventory", "move", "fighter", "alignment", "equipment"}:
            if not obj.getComponent(dep):
                # todo: better exception
                raise Exception("InputController needs object with " + dep + " component")
            
            setattr(self, dep, obj.getComponent(dep))
        
        obj.addListener("roomjoin", self.roomJoin)
    
    def roomJoin(self, o, roomData, stamp):
        self.roomData = roomData
        self.controlEvent = roomData.getEvent("control")
        self.controlEvent.addListener(self.control)
    
    def addAction(self, action):
        self.actions.append(action)
    
    
    def control(self):
        self.hasInteracted = False
        self.hasAttacked = False
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
            if len(action) > 1:
                arg = action[1]
            else:
                arg = None
            self.handlers[kind](arg)
        else:
            print("invalid action", action)
    
    def do_move(self, direction):
        if direction not in {"north", "south", "east", "west"}:
            return
        self.move.move(direction)
    
    def do_take(self, rank):
        objects = self.owner.getNearObjects()
        if rank is not None:
            if rank not in range(len(objects)):
                return
            objects = [objects[rank]]
        for obj in objects:
            if obj.getComponent("item") is not None and self.inventory.canAdd(obj):
                self.owner.trigger("take", obj)
                obj.remove()
                break
    
    def do_drop(self, rank):
        items = self.inventory.getItems()
        if rank is None:
            rank = 0
        if rank not in range(len(items)):
            return
        obj = items[rank]
        self.inventory.drop(obj)
        obj.construct(self.roomData, preserve=True)
        obj.place(self.owner.getGround())
        
    def do_use(self, rank):
        items = self.inventory.getItems()
        if rank is None:
            rank = 0
        if rank not in range(len(items)):
            return
        obj = items[rank]
        obj.getComponent("item").use(self.owner)
    
    def do_unequip(self, rank):
        slots = sorted(self.equipment.getSlots().items())
        if rank is not None:
            if rank not in range(len(slots)):
                return
            slots = [slots[rank]]
        for (slot, item) in slots:
            if item is not None and self.inventory.canAdd(item):
                self.equipment.unEquip(slot)
                self.owner.trigger("take", item)
    
    def do_interact(self, direction):
        if self.hasInteracted:
            return
        nearPlaces = self.owner.getGround().getNeighbours()
        if direction is None:
            objects = self.owner.getNearObjects()
        elif direction in nearPlaces:
            objects = nearPlaces[direction].getObjs()
        elif isinstance(direction, int):
            objects = nearPlaces[direction].getObjs()
            rank = direciton
            if rank not in range(len(objects)):
                return
            objects = [objects[rank]]
        else:
            return
        for obj in objects:
            if obj.getComponent("interact") is not None:
                obj.getComponent("interact").interact(self.owner)
                self.hasInteracted = True
                break
    
    def do_attack(self, direction):
        if self.hasAttacked:
            return
        nearPlaces = self.owner.getGround().getNeighbours()
        if direction is None:
            objs = self.owner.getNearObjects()
        elif direction in nearPlaces:
            objs = nearPlaces[direction].getObjs()
        else:
            return
        for obj in objs:
            if obj.getComponent("fighter") is not None and self.alignment.isEnemy(obj):
                self.fighter.attack(obj)
                self.hasAttacked = True
                break
    
    def do_say(self, text):
        if type(text) != str:
            return
        self.roomData.getEvent("sound").trigger(self.owner, text)
    
    def getInteractions(self):
        return []
    
    def remove(self):
        self.controlEvent.removeListener(self.control)


