
from .component import Component
from .. import gameobjects

class Change(Component):
    """ Objects that change type on interaction.
    
    This could probably also be implemented with a combination of harvest and loot,
    but this seemed better."""
    
    def __init__(self, into, nextArgs=None, nextKwargs=None):
        
        self.into = into
        self.nextArgs = nextArgs or []
        self.nextKwargs = nextKwargs or {}
    
    def attach(self, obj):
        self.owner = obj
        obj.addListener("roomjoin", self.roomJoin)
    
    def roomJoin(self, o, roomData):
        self.roomData = roomData
    
    def interact(self, obj):
        obj = gameobjects.makeEntity(self.into, self.roomData, *self.nextArgs, preserve=self.owner.isPreserved(), **self.nextKwargs)
        obj.place(self.owner.getGround())
        self.owner.remove()
