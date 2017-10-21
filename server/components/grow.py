
import timeout
import gameobjects


class Growing:
    
    
    def __init__(self, nextStage, duration, stepsPassed=0, nextArgs=[], nextKwargs={}):
        
        self.nextStage = nextStage
        self.duration = duration
        self.stepsPassed = stepsPassed
        self.nextArgs = nextArgs
        self.nextKwargs = nextKwargs
    
    
    def attach(self, obj, events):
        self.owner = obj
        self.roomEvents = events
        self.timeout = timeout.Timeout(events["update"], self.duration - self.stepsPassed, self.grow)
    
    def grow(self, to):
        
        obj = gameobjects.makeEntity(self.nextStage, self.roomEvents, *self.nextArgs, **self.nextKwargs)
        obj.place(self.owner.getGround())
        
        self.owner.trigger("grow", obj)
        print("{} has grown into {}".format(self.owner.getName(), obj.getName()))
        
        self.owner.remove()
    
    def remove(self):
        self.timeout.remove()
