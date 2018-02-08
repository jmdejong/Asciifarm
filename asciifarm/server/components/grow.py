
from .. import gameobjects
import random
from .component import Component


class Growing(Component):
    
    
    def __init__(self, nextStage, duration=None, targetTime=None, nextArgs=None, nextKwargs=None, stepsPassed=None):
        # stepsPassed is not used anymore, but included for backwards compatibility
        
        self.nextStage = nextStage
        
        # if both duration and targetTime are passed, duration is ignored
        # if both are none, the growth will never happen
        self.duration = duration
        self.targetTime = targetTime
        self.nextArgs = nextArgs or []
        self.nextKwargs = nextKwargs or {}
    
    
    def attach(self, obj):
        self.owner = obj
        obj.addListener("roomjoin", self.roomJoin)
    
    def roomJoin(self, o, roomData):
        self.roomData = roomData
        if not self.targetTime and self.duration:
            duration = int(random.triangular(self.duration/2, self.duration*2, self.duration))
            self.targetTime = roomData.getStamp() + duration
        self.roomData.setAlarm(self.targetTime, self.grow)
    
    def grow(self):
        
        obj = gameobjects.makeEntity(self.nextStage, self.roomData, *self.nextArgs, preserve=self.owner.isPreserved(), **self.nextKwargs)
        obj.place(self.owner.getGround())
        
        self.owner.trigger("grow", obj)
        print("{} has grown into {}".format(self.owner.getName(), obj.getName()))
        
        self.owner.remove()
    
    
    
    def toJSON(self):
        return {
            "nextStage": self.nextStage,
            "duration": self.duration,
            "targetTime": self.targetTime,
            "nextArgs": self.nextArgs,
            "nextKwargs": self.nextKwargs
        }
    
