
from .component import Component

class Healing(Component):
    
    """ A component to automatically heal its entity over time"""
    
    def __init__(self, interval, amount=1):
        """ interval is the number of steps until next healing, amount is the amount of health that gets added in a healing """
        self.interval = interval
        self.amount = amount
        self.delay = 0
        self.isHealing = False
    
    def attach(self, obj):
        
        if not obj.getComponent("fighter"):
            # todo: better exception
            raise Exception("Healing Component needs object with fighter component")
            
        self.fighter = obj.getComponent("fighter")
        obj.addListener("damage", self.onDamage)
        obj.addListener("roomjoin", self.roomJoin)
    
    def roomJoin(self, o, roomData):
        self.timeEvent = roomData.getEvent("update")
        self.startHealing()
    
    def onDamage(self, o, *data):
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
    
    def toJSON(self):
        return {
            "interval": self.interval,
            "amount": self.amount
        }
        
