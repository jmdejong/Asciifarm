
from .component import Component

class InputController(Component):
    
    def __init__(self):
        self.actions = [] #queue.Queue()
    
    def attach(self, obj, roomData):
        self.owner = obj
        self.roomData = roomData
        
        for dep in {"inventory", "move", "fighter", "alignment"}:
            if not obj.getComponent(dep):
                # todo: better exception
                raise Exception("InputController needs object with " + dep + " component")
            
            setattr(self, dep, obj.getComponent(dep))
        
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
        
        # probably time to make this a dict with the action as keys and the function as value
        
        if kind == "move" and len(action) > 1:
            self.move.move(action[1])
        
        
        if kind == "take":
            for obj in self.owner.getNearObjects():
                if obj.getComponent("item") != None and self.inventory.canAdd(obj):
                    self.owner.trigger("take", obj)
                    obj.remove()
                    break
        
        if kind == "drop":
            for obj in self.inventory.getItems():
                self.inventory.drop(obj)
                obj.construct(self.roomData, preserve=True)
                obj.place(self.owner.getGround())
                break
        
        
        if kind == "attack":
            nearPlaces = self.owner.getGround().getNeighbours()
            if len(action) > 1 and action[1] in nearPlaces:
                objs = nearPlaces[action[1]].getObjs()
            else:
                objs = self.owner.getNearObjects()
            for obj in objs:
                if obj.getComponent("fighter") != None and self.alignment.isEnemy(obj):
                    self.fighter.attack(obj)
                    break
        
        
        if kind == "use":
            for obj in self.inventory.getItems():
                obj.getComponent("item").use(self.owner)
                break
        
        
        if kind == "interact":
            for obj in self.owner.getNearObjects():
                if obj.getComponent("interact") != None:
                    obj.getComponent("interact").interact(self.owner)
                    break
        
        if kind == "say":
            self.roomData.getEvent("sound").trigger(self.owner, action[1])
    
    def getInteractions(self):
        return []
    
    def remove(self):
        self.controlEvent.removeListener(self.control)


