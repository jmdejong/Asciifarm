from .. import timeout
from .. import gameobjects
import random
from .component import Component


class Growing(Component):
    
    
    def __init__(self, nextStage, duration, stepsPassed=None, nextArgs=[], nextKwargs={}):
        
        self.nextStage = nextStage
        self.duration = duration if stepsPassed != None else int(random.triangular(duration/2, duration*2, duration))
        self.stepsPassed = stepsPassed or 0
        self.nextArgs = nextArgs
        self.nextKwargs = nextKwargs
    
    
    def attach(self, obj, roomData):
        self.owner = obj
        self.roomData = roomData
        self.timeout = timeout.Timeout(roomData.getEvent("update"), self.duration - self.stepsPassed, self.grow)
    
    def grow(self, to):
        
        obj = gameobjects.makeEntity(self.nextStage, self.roomData, *self.nextArgs, preserve=self.owner.isPreserved(), **self.nextKwargs)
        obj.place(self.owner.getGround())
        
        self.owner.trigger("grow", obj)
        print("{} has grown into {}".format(self.owner.getName(), obj.getName()))
        
        self.owner.remove()
    
    def remove(self):
        self.timeout.remove()
    
    
    def toJSON(self):
        return {
            "nextStage": self.nextStage,
            "duration": self.duration,
            "stepsPassed": self.stepsPassed,
            "nextArgs": self.nextArgs,
            "nextKwargs": self.nextKwargs
        }
    
