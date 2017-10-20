

class Trap:
    
    
    def attach(self, obj, events):
        
        if not obj.getComponent("fighter"):
            # todo: better exception
            raise Exception("Trap needs object with fighter component")
        
        self.owner = obj
        self.fighter = obj.getComponent("fighter")
    
    def onEnter(self, obj):
        self.fighter.attack(obj)

