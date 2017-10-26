

class Trap:
    
    
    def attach(self, obj, roomData):
        
        if not obj.getComponent("fighter"):
            # todo: better exception
            raise Exception("Trap needs object with fighter component")
        
        self.owner = obj
        self.fighter = obj.getComponent("fighter")
        
        obj.addListener(self.onObjEvent)
        
    
    def onObjEvent(self, owner, action, obj=None, *data):
        if action == "objectenter":
            self.fighter.attack(obj)
    

