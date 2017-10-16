
import random
import ground
import playerent
import gameobjects
from gameobjects import Wall
import grid
import event

_listType = type([])
_stringType = type("hello")
_noneType = type(None)
_tupleType = type(())
_dictType = type({})

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
                if not isinstance(val, _listType) :
                    val = [val]
                for obj in val:
                    if isinstance(obj, _stringType):
                        self.addObj((x, y), gameobjects.makeObject(obj))
                    elif isinstance(obj, _dictType):
                        objtype = obj["type"]
                        args = obj.get("args", [])
                        kwargs = obj.get("kwargs", {})
                        self.addObj((x, y), gameobjects.makeObject(objtype, self, (x, y), *args, **kwargs))
        
    
    def getEntrance(self):
        return self.entrance
    
    def getController(self, name):
        return self.players[name].getControlInterface()
    
    def update(self):
        self.updateEvent.trigger()
        #for listener in frozenset(self.updateListeners.values()):
            #listener()
    
    def addUpdateListener(self, listener, key=None):
        self.updateEvent.addListener(listener, key)
        #if (key == None):
            #key = listener
        #self.updateListeners[key] = listener
    
    def removeUpdateListener(self, key):
        self.updateEvent.removeListener(key)
        #self.updateListeners.pop(key, None)
    
    def getChar(self, pos):
        #x, y = pos
        return self._getGround(pos).getTopObj().getChar()
    
    def isValidPos(self, pos):
        x, y = pos
        return x >= 0 and y >= 0 and x < self.width and y < self.height
    
    def _getGround(self, pos):
        if pos not in self.field and self.isValidPos(pos):
            groundPatch = ground.GroundPatch()
            self.field[pos] = groundPatch
        return self.field.get(pos)
    
    #def get(self, pos):
        #return self._getGround(pos)
    
    def getPlace(self, place):
        return self.places.get(place)
    
    def addObj(self, pos, obj):
        self._getGround(pos).addObj(obj)
    
    def removeObj(self, pos, obj):
        self._getGround(pos).removeObj(obj)
    
    def getObjs(self, pos):
        return self._getGround(pos).getObjs()
    
    def accessible(self, pos):
        ground = self._getGround(pos)
        return ground and ground.accessible()
    
    def onEnter(self, pos, obj):
        self._getGround(pos).onEnter(obj)

