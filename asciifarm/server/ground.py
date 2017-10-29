import random

from . import event

neighbourdirs = {"north":(0,-1), "south":(0,1), "east":(1,0), "west":(-1,0)}


class GroundPatch:
    
    def __init__(self, room, pos):
        self.objects = []
        self.room = room
        self.pos = pos
        self.neighbours = None
        self.event = event.Event()
    
    def getFlags(self):
        return set().union(*[obj.getFlags() for obj in self.getObjs()])
    
    def accessible(self):
        flags = self.getFlags()
        return "floor" in flags and "solid" not in flags
    
    def addObj(self, obj):
        oldTop = self._getTopObj()
        self.objects.append(obj)
        self.objects.sort(key=(lambda o: -o.getHeight()))
        if self._getTopObj() != oldTop:
            self.event.trigger("changesprite", self.getPos(), self.getTopSprite())
        self.onEnter(obj)
    
    def removeObj(self, obj):
        oldTop = self._getTopObj()
        if obj in self.objects:
            self.objects.remove(obj)
            if obj == oldTop:
                self.event.trigger("changesprite", self.getPos(), self.getTopSprite())
        self.onLeave(obj)
    
    def getTopSprite(self):
        topObj = self._getTopObj()
        if topObj:
            return topObj.getSprite()
        else:
            return ' '
    
    def getObjs(self):
        return tuple(self.objects)
    
    def _getTopObj(self):
        return self.objects[0] if len(self.objects) else None
    
    def onEnter(self, obj):
        for o in frozenset(self.objects):
            if o == obj:
                continue
            o.trigger("objectenter", obj)
    
    def onLeave(self, obj):
        for o in frozenset(self.objects):
            if o == obj:
                continue
            o.trigger("objectleave", obj)
    
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
    
    
    def addListener(self, callback, key=None):
        self.event.addListener(callback, key)
    
    def removeListener(self, key):
        self.event.removeListener(key)

