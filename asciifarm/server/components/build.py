from .. import gameobjects


class Build:
    """ item type for item that can be placed on the map to become something more static (like buildable walls or crops)"""
    
    def __init__(self, objType, objArgs=[], objKwargs={}, flagsNeeded=set()):
        self.buildType = objType
        self.buildArgs = objArgs
        self.buildKwargs = objKwargs
        self.flagsNeeded = flagsNeeded
    
    def attach(self, obj, roomData):
        
        self.owner = obj
        self.roomData = roomData
    
    
    def use(self, user):
        groundFlags = user.getGround().getFlags()
        if not self.flagsNeeded <= groundFlags: # <= means subset when applied on sets
            return
        obj = gameobjects.makeEntity(self.buildType, self.roomData, *self.buildArgs, **self.buildKwargs)
        obj.place(user.getGround())
        self.owner.trigger("drop")
    