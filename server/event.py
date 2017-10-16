


class Event:
    
    def __init__(self):
        self.listeners = {}
    
    def addListener(self, listener, key=None):
        if key == None:
            key = listener
        self.listeners[key] = listener
    
    def removeListener(self, key):
        self.listeners.pop(key)
    
    def trigger(self, *args, **kwargs):
        for listener in frozenset(self.listeners.values()):
            listener(*args, **kwargs)
