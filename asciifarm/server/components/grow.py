
from .. import gameobjects
import random
from .component import Component
from ..template import Template


class Growing(Component):
    
    
    def __init__(self, nextStage, duration=None, targetTime=None, nextArgs=None, nextKwargs=None, stepsPassed=None):
        # stepsPassed is not used anymore, but included for backwards compatibility
        
        #self.nextStage = nextStage
        if nextArgs is None:
            nextArgs = []
        if nextKwargs is None:
            nextKwargs = {}
        self.next = Template(nextStage, *nextArgs, **nextKwargs)
        
        # if both duration and targetTime are passed, duration is ignored
        # if both are none, the growth will never happen
        self.duration = duration
        self.targetTime = targetTime
        #self.nextArgs = nextArgs or []
        #self.nextKwargs = nextKwargs or {}
        
    
    
    def attach(self, obj):
        self.owner = obj
        obj.addListener("roomjoin", self.roomJoin)
    
    def roomJoin(self, o, roomData, stamp):
        self.roomData = roomData
        if self.targetTime is None and self.duration:
            duration = int(random.triangular(self.duration/2, self.duration*2, self.duration))
            self.targetTime = stamp + duration
        self.roomData.setAlarm(self.targetTime, self.grow)
    
    def grow(self):
        
        obj = gameobjects.createEntity(self.next)#{"type": self.nextStage, "args": self.nextArgs, "kwargs": self.nextKwargs})
        obj.construct(self.roomData, preserve=self.owner.isPreserved(), stamp=self.targetTime)
        obj.place(self.owner.getGround())
        
        self.owner.trigger("grow", obj)
        print("{} has grown into {}".format(self.owner.getName(), obj.getName()))
        
        self.owner.remove()
    
    def getTargetTime(self):
        return self.targetTime
    
    def toJSON(self):
        return {
            "nextStage": self.nextStage,
            "duration": self.duration,
            "targetTime": self.targetTime,
            "nextArgs": self.nextArgs,
            "nextKwargs": self.nextKwargs
        }
    
