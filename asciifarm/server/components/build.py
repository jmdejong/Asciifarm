
from .. import gameobjects
from .component import Component
from ..template import Template

class Build(Component):
    """ item type for item that can be placed on the map to become something more static (like buildable walls or crops)"""
    
    def __init__(self, objType, objArgs=(), objKwargs=None, flagsNeeded=frozenset(), blockingFlags=frozenset()):
        if objKwargs is None:
            objKwargs = {}
        self.buildTemplate = Template(objType, *objArgs, **objKwargs)
        self.flagsNeeded = set(flagsNeeded)
        self.blockingFlags = set(blockingFlags)
    
    def attach(self, obj):
        self.owner = obj
        obj.addListener("roomjoin", self.roomJoin)
    
    def roomJoin(self, obj, roomData, stamp):
        self.roomData = roomData
    
    
    def use(self, user):
        groundFlags = user.getGround().getFlags()
        if not self.flagsNeeded <= groundFlags or groundFlags & self.blockingFlags: # <= means subset when applied on sets
            # groundFlags must contain all of self.flagsNeeded, and none of self.blockingFlags
            return
        roomData = user.getRoomData()
        obj = gameobjects.buildEntity(self.buildTemplate, roomData, preserve=True)
        obj.place(user.getGround())
        self.owner.trigger("drop")
        
    def toJSON(self):
        return {
            "objType": self.buildType,
            "objArgs": self.buildArgs,
            "objKwargs": self.buildKwargs,
            "flagsNeeded": list(self.flagsNeeded),
            "blockingFlags": list(self.blockingFlags)
        }
    
