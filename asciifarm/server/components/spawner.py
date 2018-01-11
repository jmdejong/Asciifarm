from .. import gameobjects
from .. import timeout
import random
from .component import Component


class Spawner(Component):
    
    def __init__(self, objectType, amount=1, respawnDelay=1, setHome=False, initialSpawn=False, objectArgs=None, objectKwargs=None):
        if objectArgs is None:
            objectArgs = []
        if objectKwargs is None:
            objectKwargs = {}
        self.objectType = objectType
        self.amount = amount
        self.respawnDelay = respawnDelay
        self.spawned = set()
        self.objectArgs = objectArgs
        self.objectKwargs = objectKwargs
        self.timeouts = set()
        self.setHome = setHome
        self.initialSpawn = initialSpawn
    
    def attach(self, obj):
        
        self.owner = obj
        obj.addListener("roomjoin", self.roomJoin)
    
    def roomJoin(self, o, roomData):
        self.roomData = roomData
        self.updateEvent = roomData.getEvent("update")
        
        for i in range(self.amount):
            if self.initialSpawn:
                self.goSpawn(1)
            else:
                self.goSpawn()
    
    def goSpawn(self, duration=None):
        if duration is None:
            duration = self.respawnDelay
        to = timeout.Timeout(self.updateEvent, random.triangular(duration/2, duration*2, duration), callback=self.spawn)
        self.timeouts.add(to)
    
    def spawn(self, to=None):
        objectKwargs = self.objectKwargs.copy()
        if self.setHome:
            objectKwargs["home"] = self.owner
        obj = gameobjects.makeEntity(self.objectType, self.roomData, *self.objectArgs, **objectKwargs)
        obj.place(self.owner.getGround())
        self.spawned.add(obj)
        if to:
            self.timeouts.remove(to)
        obj.addListener("remove", self.onSpawnedRemove)
        print("{} spawned a {}".format(self.owner.getName(), self.objectType))
    
    def onSpawnedRemove(self, obj, *data):
        """ handle spawned object death """
        self.spawned.remove(obj)
        obj.removeListener("remove", self.onSpawnedRemove)
        self.goSpawn()
    
    def remove(self):
        for to in self.timeouts:
            to.remove()
    
    
    def toJSON(self):
        return {
            "objectType": self.objectType,
            "amount": self.amount,
            "respawnDelay": self.respawnDelay,
            "setHome": self.setHome,
            "objectArgs": self.objectArgs,
            "objectKwargs": self.objectKwargs,
            "initialSpawn": self.initialSpawn
        } # it won't keep track of spawned entities. It will just spawn new entities again
    

