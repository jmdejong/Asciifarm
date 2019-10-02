
from .dc import DC
from ..template import Template


class Serialise(DC):
    
    def __init__(self, func):
        self.func = func
    
    def serialise(self, obj, roomData):
        return func(obj, roomData)
    

def Static(name, *args, **kwargs):
    template = Template(name, *args, **kwargs)
    return Serialise(lambda obj, roomData: template)
