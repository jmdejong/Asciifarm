import random

from .eventtarget import EventTarget

neighbourdirs = {"north":(0,-1), "south":(0,1), "east":(1,0), "west":(-1,0)}


class GroundPatch:
    
    def __init__(self, room, pos):
        self.objects = []
        self.room = room
        self.pos = pos
        self.neighbours = None
        self.event = EventTarget()
    
    def getFlags(self):
        return set().union(*[obj.getFlags() for obj in self.getObjs()])
    
    def accessible(self):
        flags = self.getFlags()
        return "floor" in flags and "solid" not in flags
    
    def addObj(self, obj):
        self.objects.append(obj)
        self.objects.sort(key=(lambda o: -o.getHeight()))
        self.trigger("changesprite")
        self.onEnter(obj)
    
    def removeObj(self, obj):
        if obj in self.objects:
            self.objects.remove(obj)
            self.trigger("changesprite")
            self.onLeave(obj)
    
    def getSprites(self):
        sprites = [obj.getSprite() for obj in self.objects if obj.getSprite()]
        return sprites
    
    def getObjs(self):
        return list(self.objects)
    
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
    
    def trigger(self, event, *data):
        self.event.trigger(event, self, *data)
    
    def addListener(self, event, callback, key=None):
        self.event.addListener(event, callback, key)
    
    def removeListener(self, event, key):
        self.event.removeListener(event, key)
    
    def __getstate__(self):
        state = self.__dict__.copy()
        state["neighbours"] = None
        return state

