
import random
import event

neighbourdirs = {"north":(0,-1), "south":(0,1), "east":(1,0), "west":(-1,0)}

class GroundPatch:
    
    def __init__(self, room, pos, sprite=' '):
        self.objects = set()
        self.sprite = sprite
        self.room = room
        self.pos = pos
        self.neighbours = None
        self.event = event.Event()
    
    def accessible(self):
        return not any(obj.isSolid() for obj in self.objects)
    
    def addObj(self, obj):
        if obj.getHeight() >= self.getTopObj().getHeight():
            self.event.trigger("changesprite", self.getPos(), obj.getSprite())
        self.objects.add(obj)
    
    def removeObj(self, obj):
        if obj in self.objects:
            self.objects.remove(obj)
            topObj = self.getTopObj()
            if obj.getHeight() >= topObj.getHeight():
                self.event.trigger("changesprite", self.getPos(), topObj.getSprite())
    
    def getObjs(self):
        return frozenset(self.objects)
    
    def getTopObj(self):
        topObj = self
        for obj in self.getObjs():
            if obj.getHeight() > topObj.getHeight():
                topObj = obj
        return topObj
    
    def getSprite(self):
        return self.sprite
    
    def onEnter(self, obj):
        for o in frozenset(self.objects):
            if o == obj:
                continue
            o.trigger("objectenter", obj)
    
    def getNeighbours(self):
        if not self.neighbours:
            x, y = self.pos
            self.neighbours = {}
            for name, (dx, dy) in neighbourdirs.items():
                g = self.room.get((x+dx, y+dy))
                if g:
                    self.neighbours[name] = g
        
        return self.neighbours
    
    def getPos(self):
        return self.pos
    
    def getHeight(self):
        return -1
    
    
    def addListener(self, callback, key=None):
        self.event.addListener(callback, key)
    
    def removeListener(self, key):
        self.event.removeListener(key)

