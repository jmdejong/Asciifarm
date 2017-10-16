
import random
import ground
import playerent
import gameobjects
from gameobjects import Wall
import grid
import event


class Room:
    
    
    def __init__(self, name, data):
        self.name = name
        self.players = {}
        self.width = data["width"]
        self.height = data["height"]
        self.updateEvent = event.Event()
        self.entrance = tuple(data["spawn"])
        
        self.places = data.get("places", {})
        
        self.field = {}
        
        g = grid.fromDict(data)
        for x in range(g.width):
            for y in range(g.height):
                val = g.get(x, y)
                if not isinstance(val, list) :
                    val = [val]
                for obj in val:
                    if isinstance(obj, str):
                        objtype = obj
                        args = []
                        kwargs = {}
                    elif isinstance(obj, dict):
                        objtype = obj["type"]
                        args = obj.get("args", [])
                        kwargs = obj.get("kwargs", {})
                    else:
                        continue
                    self.addObj((x, y), gameobjects.makeObject(objtype, self, *args, **kwargs))
        
    
    def getEntrance(self):
        return self.entrance
    
    def getController(self, name):
        return self.players[name].getControlInterface()
    
    def update(self):
        self.updateEvent.trigger()
    
    def addUpdateListener(self, listener, key=None):
        self.updateEvent.addListener(listener, key)
    
    def removeUpdateListener(self, key):
        self.updateEvent.removeListener(key)
    
    def getChar(self, pos):
        return self._getGround(pos).getTopObj().getChar()
    
    def isValidPos(self, pos):
        x, y = pos
        return x >= 0 and y >= 0 and x < self.width and y < self.height
    
    def _getGround(self, pos):
        if pos not in self.field and self.isValidPos(pos):
            groundPatch = ground.GroundPatch(self, pos)
            self.field[pos] = groundPatch
        return self.field.get(pos)
    
    def get(self, pos):
        if isinstance(pos, str):
            pos = self.places.get(pos)
        if pos:
            return self._getGround(pos)
        return None
    
    def getPlace(self, place):
        return self.places.get(place)
    
    def addObj(self, pos, obj):
        obj.place(self.get(pos))
    
    def removeObj(self, pos, obj):
        self._getGround(pos).removeObj(obj)

