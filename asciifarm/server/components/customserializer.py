

from .component import Component

class CustomSerializer(Component):
    
    def __init__(self, fn):
        self.fn = fn
    
    def attach(self, obj):
        self.owner = obj
    
    def serialize(self):
        return fn(self.owner)
