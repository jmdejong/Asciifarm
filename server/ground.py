
import random
from gameobjects import objectdict

neighbourdirs = {"north":(0,-1), "south":(0,1), "east":(1,0), "west":(-1,0)}

class GroundPatch:
    
    #height = 0
    size = 0
    char = ' '
    objects = None
    
    def __init__(self, room, pos, char=' '):
        # objects is actually a set, but because its elements are mutable
        # it is implemented as a dictionary with the id as index
        self.objects = {}
        self.char = char
        self.room = room
        self.pos = pos
        self.neighbours = None
    
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
    
    def getNeighbours(self):
        if not self.neighbours:
            x, y = self.pos
            self.neighbours = {}
            for name, (dx, dy) in neighbourdirs.items():
                g = self.room.get((x+dx, y+dy))
                if g:
                    self.neighbours[name] = g
        
        return self.neighbours
    

