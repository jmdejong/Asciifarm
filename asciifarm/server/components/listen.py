
from .component import Component


class Listen(Component):
    
    
    def attach(self, obj, roomData):
        self.owner = obj
        
        self.soundEvent = roomData.getEvent("sound")
        self.soundEvent.addListener(self.notify)
        self.roomData = roomData
    
    
    def notify(self, source, text):
        print(source, text)
        self.owner.trigger("sound", source, text)
    
    def remove(self):
        self.soundEvent.removeListener(self.notify)
