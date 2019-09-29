
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
        
        if not obj.dataComponents.get("attackable"):
            # todo: better exception
            raise Exception("Healing Component needs object with attackable component")
            
        self.fighter = obj.dataComponents.get("attackable")
        obj.addListener("damage", self.onDamage)
        obj.addListener("roomjoin", self.roomJoin)
    
    def roomJoin(self, o, roomData, stamp):
        self.roomData = roomData
        self.startHealing(stamp)
    
    def onDamage(self, o, *data):
        self.startHealing()
    
    def startHealing(self, start=None):
        """ start healing if it is not happening already """
        if not self.isHealing and not self.fighter.healthFull():
            if start is None:
                start = self.roomData.getStamp()
            self.roomData.setAlarm(start + self.interval, self.heal)
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
        
