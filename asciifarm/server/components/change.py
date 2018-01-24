
from .component import Component
from .. import gameobjects

class Change(Component):
    """ Objects that change type on interaction.
    
    This could probably also be implemented with a combination of harvest and loot,
    but this seemed better."""
    
    def __init__(self, into, permitted=None, nextArgs=None, nextKwargs=None):
        
        self.into = into
        self.nextArgs = nextArgs or []
        self.nextKwargs = nextKwargs or {}
        
        self.permitted = permitted
    
    def attach(self, obj):
        self.owner = obj
        obj.addListener("roomjoin", self.roomJoin)
    
    def roomJoin(self, o, roomData):
        self.roomData = roomData
    
    def interact(self, other):
        if self.permitted is not None and other.getName() not in self.permitted:
            return
        obj = gameobjects.makeEntity(self.into, self.roomData, *self.nextArgs, preserve=self.owner.isPreserved(), **self.nextKwargs)
        
        obj.place(self.owner.getGround())
        self.owner.remove()
    
    def toJSON(self):
        return {
            "into": self.into,
            "permitted": self.permitted,
            "nextArgs": self.nextArgs,
            "nextKwargs": self.nextKwargs
        }
