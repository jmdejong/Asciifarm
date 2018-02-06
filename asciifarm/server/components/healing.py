
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
        self.roomData = roomData
        self.startHealing()
    
    def onDamage(self, o, *data):
        self.startHealing()
    
    def startHealing(self):
        """ start healing if it is not happening already """
        if not self.isHealing and not self.fighter.healthFull():
            self.roomData.setAlarm(self.roomData.getStamp() + self.interval, self.heal)
            self.isHealing = True
    
    def heal(self):
        if self.fighter.healthFull():
            return
        self.fighter.heal(self.amount, None)
        self.isHealing = False
        self.startHealing()
    
    
    def toJSON(self):
        return {
            "interval": self.interval,
            "amount": self.amount
        }
        
