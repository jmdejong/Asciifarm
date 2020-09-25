
from .component import Component

class InputController(Component):
    
    def __init__(self):
        self.action = None
        
        self.handlers = {
            "move": self.do_move,
            "take": self.do_take,
            "drop": self.do_drop,
            "use": self.do_use,
            "unequip": self.do_unequip,
            "interact": self.do_interact,
            "attack": self.do_attack,
            "say": self.do_say,
            "pick": self.do_pick
        }
        self.target = None
            
    
    def attach(self, obj):
        self.owner = obj
        
        for dep in {"inventory", "move", "fighter", "alignment", "equipment", "select"}:
            if not obj.getComponent(dep):
                # todo: better exception
                raise Exception("InputController needs object with " + dep + " component")
            
            setattr(self, dep, obj.getComponent(dep))
        
        obj.addListener("roomjoin", self.roomJoin)
        obj.addListener("damage", self.retaliate)
    
    def roomJoin(self, o, roomData, stamp):
        self.roomData = roomData
        self.controlEvent = roomData.getEvent("control")
        self.controlEvent.addListener(self.control)
    
    def setAction(self, action):
        self.action = action
    
    
    def control(self):
        action = self.action
        if action:
            self.target = None
        self.action = None
        if action is not None:
            self.executeAction(action)
        if self.target:
            self.fighter.attack(self.target)
    
    def executeAction(self, action):
        
        kind = action[0]
        if len(action) > 1:
            arg = action[1]
        else:
            arg = None
        try:
            handler = self.handlers.get(kind)
        except TypeError:
            handler = None
        if handler is None:
            print("invalid action", action)
            return
        handler(arg)
    
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
            return False
        obj = items[rank]
        self.inventory.drop(obj)
        obj.construct(self.roomData, preserve=True)
        obj.place(self.owner.getGround())
        return True
        
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
    
    def do_interact(self, directions):
        objects = self._getNearbyObjects(directions)
        for obj in objects:
            if obj.getComponent("interact") is not None:
                obj.getComponent("interact").interact(self.owner)
                break
    
    def do_attack(self, directions):
        objects = self._getNearbyObjects(directions)
        if self.target in objects:
            objects = {self.target}
        for obj in objects:
            if self.fighter.canAttack(obj) and self.alignment.isEnemy(obj):
                self.fighter.attack(obj)
                self.target = obj
                break
    
    def do_say(self, text):
        if type(text) != str:
            return
        self.roomData.getEvent("sound").trigger(self.owner, text)
    
    def do_pick(self, option):
        selected = self.select.getSelected()
        if selected is None:
            return
        optionmenu = selected.getComponent("options")
        if optionmenu is None:
            return
        optionmenu.choose(option, self.owner)
    
    def _getNearbyObjects(self, directions):
        nearPlaces = self.owner.getGround().getNeighbours()
        if not isinstance(directions, list):
            directions = [directions]
        objects = []
        for direction in directions:
            if direction == "" or direction == "none":
                objects += self.owner.getNearObjects()
            elif isinstance(direction, str) and direction in nearPlaces:
                objects += nearPlaces[direction].getObjs()
        return objects
        
    
    def getInteractions(self):
        return []
    
    def remove(self):
        self.controlEvent.removeListener(self.control)
    
    def retaliate(self, _self, attacker, damage):
        self.target = attacker


