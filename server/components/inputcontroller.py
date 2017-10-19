
import queue

class InputController:
    
    def __init__(self):
        self.actions = queue.Queue()
    
    def attach(self, obj, events):
        self.owner = obj
        
        for dep in {"inventory", "move", "fighter", "alignment"}:
            if not obj.getComponent(dep):
                # todo: better exception
                raise Exception("InputController needs object with " + dep + " component")
        
        self.controlEvent = events["control"]
        self.controlEvent.addListener(self.control)
    
    def addAction(self, action):
        self.actions.put(action)
    
    
    def control(self, steps):
        while not self.actions.empty():
            action = self.actions.get()
            self.executeAction(action)
    
    def executeAction(self, action):
        if not action or len(action) < 1:
            return
        kind = action[0]
        if kind == "move" and len(action) > 1:
            self.owner.getComponent("move").move(action[1])
        
        inventory = self.owner.getComponent("inventory")
        
        if kind == "take":
            for obj in self.owner.getNearObjects():
                if obj.getComponent("item") != None and inventory.canAdd(obj):
                    inventory.add(obj)
                    obj.remove()
                    break
        
        if kind == "drop":
            for obj in inventory.getItems():
                inventory.drop(obj)
                obj.place(self.owner.getGround())
                break
        
        
        fighter = self.owner.getComponent("fighter")
        if kind == "attack":
            nearPlaces = self.owner.getGround().getNeighbours()
            if len(action) > 1 and action[1] in nearPlaces:
                objs = nearPlaces[action[1]].getObjs()
            else:
                objs = self.owner.getNearObjects()
            for obj in objs:
                if obj.getComponent("fighter") != None and self.owner.getComponent("alignment").isEnemy(obj):
                    fighter.attack(obj)
                    break
    
    def getInteractions(self):
        return []
    
    def remove(self):
        self.controlEvent.removeListener(self.control)


