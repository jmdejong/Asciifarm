from .. import gameobjects


class Build:
    """ item type for item that can be placed on the map to become something more static (like buildable walls or crops)"""
    
    def __init__(self, objType, objArgs=[], objKwargs={}):
        self.buildType = objType
        self.buildArgs = objArgs
        self.buildKwargs = objKwargs
    
    def attach(self, obj, roomData):
        
        self.owner = obj
        self.roomData = roomData
    
    
    def use(self, user):
        obj = gameobjects.makeEntity(self.buildType, self.roomData, *self.buildArgs, **self.buildKwargs)
        obj.place(user.getGround())
        self.owner.trigger("drop")
    
