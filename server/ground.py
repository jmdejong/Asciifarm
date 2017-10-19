
import random

neighbourdirs = {"north":(0,-1), "south":(0,1), "east":(1,0), "west":(-1,0)}

class GroundPatch:
    
    def __init__(self, room, pos, sprite=' '):
        # objects is actually a set, but because its elements are mutable
        # it is implemented as a dictionary with the id as index
        self.objects = {}
        self.sprite = sprite
        self.room = room
        self.pos = pos
        self.neighbours = None
    
    def accessible(self):
        return not any(obj.isSolid() for obj in self.objects.values())
    
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
            if obj.getHeight() > topObj.getHeight():
                topObj = obj
        return topObj
    
    def getSprite(self):
        return self.sprite
    
    def onEnter(self, obj):
        for o in frozenset(self.objects.values()):
            if o == obj:
                continue
            collision = o.getComponent("collision")
            if collision:
                collision.onEnter(obj)
    
    def getNeighbours(self):
        if not self.neighbours:
            x, y = self.pos
            self.neighbours = {}
            for name, (dx, dy) in neighbourdirs.items():
                g = self.room.get((x+dx, y+dy))
                if g:
                    self.neighbours[name] = g
        
        return self.neighbours
    
    def getHeight(self):
        return -1

