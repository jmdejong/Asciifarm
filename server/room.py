
import random
import ground
import gameobjects
import grid
import event
import entity
import roomdata


class Room:
    
    
    def __init__(self, name, data):
        self.name = name
        self.width = data["width"]
        self.height = data["height"]
        self.entrance = tuple(data["spawn"])
        
        self.changedCells = {} # this probably doesn't belong in this class, but for now it will do
        # It's probably better to make the view component more elaborate
        
        self.roomData = roomdata.RoomData(events={
            "control": event.Event(),
            "move": event.Event(),
            "fight": event.Event(),
            "update": event.Event()
            })
        
        self.places = data.get("places", {})
        for name, pos in self.places.items():
            self.places[name] = tuple(pos)
        
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
                    ent = gameobjects.makeEntity(objtype, self.roomData, *args, **kwargs)
                    self.addObj((x, y), ent)
        
    
    def getEntrance(self):
        return self.entrance
    
    def update(self):
        """ call several update events for components
        
        These events are separate to ensure that everything happens in the right order
        
        'update' also has the number of steps as argument. This will be useful when room unloading becomes a thing, and when the room loads again a lot of steps have to be simulated.
        """
        self.roomData.getEvent("control").trigger()
        self.roomData.getEvent("move").trigger()
        self.roomData.getEvent("fight").trigger()
        self.roomData.getEvent("update").trigger(1)
    
    def getSprite(self, pos):
        return self._getGround(pos).getTopSprite()
    
    def isValidPos(self, pos):
        x, y = pos
        return x >= 0 and y >= 0 and x < self.width and y < self.height
    
    def _getGround(self, pos):
        if pos not in self.field and self.isValidPos(pos):
            groundPatch = ground.GroundPatch(self, pos)
            self.field[pos] = groundPatch
            groundPatch.addListener(self.onGroundChange)
        return self.field.get(pos)
    
    def get(self, pos):
        if isinstance(pos, str):
            pos = self.places.get(pos)
        if pos:
            return self._getGround(pos)
        return None
    
    def getRoomData(self):
        return self.roomData
    
    def addObj(self, pos, obj):
        obj.place(self.get(pos))
    
    def removeObj(self, pos, obj):
        self._getGround(pos).removeObj(obj)
    
    def onGroundChange(self, action, pos, sprite):
        if action == "changesprite":
            self.changedCells[pos] = sprite
    
    def getChangedCells(self):
        return self.changedCells
    
    def resetChangedCells(self):
        self.changedCells = {}
        

