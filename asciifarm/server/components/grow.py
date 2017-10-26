from .. import timeout
from .. import gameobjects


class Growing:
    
    
    def __init__(self, nextStage, duration, stepsPassed=0, nextArgs=[], nextKwargs={}):
        
        self.nextStage = nextStage
        self.duration = duration
        self.stepsPassed = stepsPassed
        self.nextArgs = nextArgs
        self.nextKwargs = nextKwargs
    
    
    def attach(self, obj, roomData):
        self.owner = obj
        self.roomData = roomData
        self.timeout = timeout.Timeout(roomData.getEvent("update"), self.duration - self.stepsPassed, self.grow)
    
    def grow(self, to):
        
        obj = gameobjects.makeEntity(self.nextStage, self.roomData, *self.nextArgs, **self.nextKwargs)
        obj.place(self.owner.getGround())
        
        self.owner.trigger("grow", obj)
        print("{} has grown into {}".format(self.owner.getName(), obj.getName()))
        
        self.owner.remove()
    
    def remove(self):
        self.timeout.remove()
