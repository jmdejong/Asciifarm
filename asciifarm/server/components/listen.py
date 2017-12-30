
from .component import Component


class Listen(Component):
    
    
    def attach(self, obj):
        self.owner = obj
        obj.addListener("roomjoin", self.roomJoin)
    
    def roomJoin(self, o, roomData):
        
        self.soundEvent = roomData.getEvent("sound")
        self.soundEvent.addListener(self.notify)
        self.roomData = roomData
    
    
    def notify(self, source, text):
        self.owner.trigger("sound", source, text)
    
    def remove(self):
        self.soundEvent.removeListener(self.notify)
