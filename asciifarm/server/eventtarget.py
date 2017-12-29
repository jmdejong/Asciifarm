
from .event import Event

class EventTarget:
    
    def __init__(self):
        
        self.events = {}
    
    def addListener(self, name, func, key=None):
        if name not in self.events:
            self.events[name] = Event()
        self.events[name].addListener(func, key)
    
    def removeListener(self, name, key):
        self.events[name].reamoveListener(key)
    
    def trigger(self, event, *args, **kwargs):
        if event in self.events:
            self.events[event].trigger(*args, **kwargs)
