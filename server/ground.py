
import random
from gameobjects import objectdict
    
class GroundPatch:
    
    #height = 0
    size = 0
    char = ' '
    objects = None
    
    def __init__(self, char=' '):
        # objects is actually a set, but because its elements are mutable
        # it is implemented as a dictionary with the id as index
        self.objects = {}
        self.char = char
    
    def accessible(self):
        return not any("solid" in obj.attributes for obj in self.objects.values())
    
    def addObj(self, obj):
        self.objects[id(obj)] = obj
    
    def removeObj(self, obj):
        if id(obj) in self.objects:
            del self.objects[id(obj)]
    
    def getObjs(self):
        return self.objects.values()
    
    def getTopObj(self):
        topObj = self
        for obj in self.getObjs():
            if obj.size > topObj.size:
                topObj = obj
        return topObj
    
    def getChar(self):
        return self.char
    
    def onEnter(self, obj):
        for o in frozenset(self.objects.values()):
            if o == obj:
                continue
            if hasattr(o, "onEnter"):
                o.onEnter(obj)
