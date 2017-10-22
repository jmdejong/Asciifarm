

class Healing:
    
    """ A component to automatically heal its entity over time"""
    
    def __init__(self, interval, amount=1):
        """ interval is the number of steps until next healing, amount is the amount of health that gets added in a healing """
        self.interval = interval
        self.amount = amount
        self.delay = 0
        self.isHealing = False
    
    def attach(self, obj, roomData):
        
        if not obj.getComponent("fighter"):
            # todo: better exception
            raise Exception("Healing Component needs object with fighter component")
            
        self.fighter = obj.getComponent("fighter")
        self.timeEvent = roomData.getEvent("update")
        obj.addListener(self.onObjEvent)
        
        self.startHealing()
    
    def onObjEvent(self, o, action, *data):
        if action == "damage":
            self.startHealing()
    
    def startHealing(self):
        """ start healing if it is not happening already """
        if not self.isHealing:
            self.delay = self.interval
            self.timeEvent.addListener(self.time)
            self.isHealing = True
    
    def time(self, steps):
        """ decrement delay, each time that delay is 0, heal the entity """
        while steps >= self.delay:
            self.fighter.heal(self.amount, None)
            steps -= self.delay
            self.delay = self.interval
            if self.fighter.healthFull():
                self.timeEvent.removeListener(self.time)
                self.isHealing = False
                return
        self.delay -= steps
    
    def remove(self):
        self.timeEvent.removeListener(self.time)
        
