import random

from . import ground
from . import gameobjects
from . import grid
from . import event
from . import entity
from . import roomdata
from . import serialize
from .template import Template


from .systems import fight, attacked, heal, move, controlai, control, handleevents, remove, droploot, clearinbox, trap, teleport, sound, checktimers, create, spawn

class Room:
    
    
    def __init__(self, name, data, preserved=None):
        self.name = name
        self.width = data["width"]
        self.height = data["height"]
        self.entrance = tuple(data["spawn"])
        
        self.changedCells = {} # this probably doesn't belong in this class, but for now it will do
        # It's probably better to make the view component more elaborate
        
        self.lastStepStamp = 0
        
        self.roomData = roomdata.RoomData()
        
        
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
                    ent = gameobjects.buildEntity(Template.fromJSON(obj), self.roomData)
                    self.addObj((x, y), ent)
        
        if preserved is not None:
            self.loadPreserved(preserved)
        
        self.resetChangedCells()
        
        
    
    def getName(self):
        return self.name
    
    def getEntrance(self):
        return self.entrance
    
    def update(self, stepStamp):
        """ call several update events for components
        
        These events are separate to ensure that everything happens in the right order
        
        'update' also has the number of steps as argument.
        If the room has been unloaded for a while, it will make a large step next.
        This is useful for allowing plants to grow for example
        """
        if self.lastStepStamp is None:
            timePassed = 1
        else:
            timePassed = stepStamp - self.lastStepStamp
        
        self.roomData.setStamp(stepStamp)
        
        self.roomData.triggerAlarms()
        
        systems = [
            control,
            controlai,
            move,
            trap,
            teleport,
            fight,
            heal,
            attacked,
            droploot,
            spawn,
            create,
            handleevents,
            checktimers,
            sound,
            clearinbox,
            remove
        ]
        for system in systems:
            system(self.roomData)
        
        self.lastStepStamp = stepStamp
    
    def getSprites(self, pos):
        return self._getGround(pos).getSprites()
    
    def isValidPos(self, pos):
        x, y = pos
        return x >= 0 and y >= 0 and x < self.width and y < self.height
    
    def _getGround(self, pos):
        if pos not in self.field and self.isValidPos(pos):
            groundPatch = ground.GroundPatch(self, pos)
            self.field[pos] = groundPatch
            groundPatch.addListener("changesprite", self.onGroundChange)
        return self.field.get(pos)
    
    def get(self, pos):
        if isinstance(pos, str):
            pos = self.places.get(pos)
        if not pos:
            return None
        return self._getGround(pos)
        
    
    def getAllObjs(self):
        return set().union(*[{(pos, obj) for obj in gr.getObjs()} for (pos, gr) in self.field.items()])
    
    def getRoomData(self):
        return self.roomData
    
    def addObj(self, pos, obj):
        if isinstance(pos, tuple) and len(pos) == 2:
            x, y = pos
            x %= self.width
            y %= self.height
            pos = (x, y)
        if obj is not None:
            place = self.get(pos)
            if place is None:
                if pos not in self.places:
                    raise Exception("Position {} does not exist in room {}. Available places: {}".format(pos, self.name, self.places))
                else:
                    raise Exception("Position {} at {} is not a valid position.".format(pos, self.places[pos]))
            obj.place(self.get(pos))
    
    def removeObj(self, pos, obj):
        self._getGround(pos).removeObj(obj)
    
    def onGroundChange(self, obj):
        self.changedCells[obj.getPos()] = self.getSprites(obj.getPos())
    
    def getChangedCells(self):
        return self.changedCells
    
    def resetChangedCells(self):
        self.changedCells = {}
    
    def getPreserved(self):
        return {
            "changes": [
                (obj.getGround().getPos(), obj.serialize().toJSON())
                for obj in self.roomData.getPreserved()],
            "step": self.lastStepStamp}
    
    def loadPreserved(self, objects):
        for (pos, objData) in objects["changes"]:
            obj = gameobjects.buildEntity(Template.fromJSON(objData), self.roomData, preserve=True)
            self.addObj(tuple(pos), obj)
        self.lastStepStamp = objects.get("step")
        self.roomData.setStamp(self.lastStepStamp)
        

