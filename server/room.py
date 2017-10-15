
import random
import ground
import playerent
import gameobjects
from gameobjects import Wall
import grid

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
        self.updateListeners = {}
        self.entrance = (10, 5)
        
        self.field = {}
        
        g = grid.fromDict(data)
        for x in range(g.width):
            for y in range(g.height):
                val = g.get(x, y)
                if isinstance(val, _stringType) :
                    val = [val]
                for obj in val:
                    if isinstance(obj, _stringType):
                        self.addObj((x, y), gameobjects.makeObject(obj))
                    elif isinstance(obj, _dictType):
                        t = obj["type"]
                        args = obj.get("args", [])
                        kwargs = obj.get("kwargs", {})
                        self.addObj((x, y), gameobjects.makeObject(objtype, *args, **kwargs))
        
        #for x in range(self.width):
            #self.addObj((x, 0), Wall())
            #self.addObj((x, self.height-1), Wall())
        #for y in range(1,self.height-1):
            #self.addObj((0, y), Wall())
            #self.addObj((self.width-1, y), Wall())
        
    
    def getEntrance(self):
        return self.entrance
    
    def getController(self, name):
        return self.players[name].getControlInterface()
    
    def update(self):
        for listener in frozenset(self.updateListeners.values()):
            listener()
    
    def addUpdateListener(self, listener, key=None):
        if (key == None):
            key = listener
        self.updateListeners[key] = listener
    
    def removeUpdateListener(self, key):
        self.updateListeners.pop(key, None)
    
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
    
    def addObj(self, pos, obj):
        self._getGround(pos).addObj(obj)
    
    def removeObj(self, pos, obj):
        self._getGround(pos).removeObj(obj)
    
    def getObjs(self, pos):
        return self._getGround(pos).getObjs()
    
    def accessible(self, pos):
        ground = self._getGround(pos)
        return ground and ground.accessible()


