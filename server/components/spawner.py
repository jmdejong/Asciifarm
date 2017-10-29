
import timeout
import gameobjects

class Spawner:
    
    def __init__(self, objectType, amount=1, respawnDelay=1, objectArgs=[], objectKwargs={}):
        self.objectType = objectType
        self.amount = amount
        self.respawnDelay = respawnDelay
        self.spawned = set()
        self.objectArgs = objectArgs
        self.objectKwargs = objectKwargs
        self.timeouts = set()
    
    def attach(self, obj, roomData):
        
        self.owner = obj
        self.roomData = roomData
        self.updateEvent = roomData.getEvent("update")
        
        for i in range(self.amount):
            self.goSpawn()
    
    def goSpawn(self):
        to = timeout.Timeout(self.updateEvent, self.respawnDelay, callback=self.spawn)
        self.timeouts.add(to)
    
    def spawn(self, to):
        obj = gameobjects.makeEntity(self.objectType, self.roomData, *self.objectArgs, home=self.owner, **self.objectKwargs)
        obj.place(self.owner.getGround())
        self.spawned.add(obj)
        self.timeouts.remove(to)
        obj.addListener(self.onObjEvent)
        print("{} spawned a {}".format(self.owner.getName(), self.objectType))
    
    def onObjEvent(self, obj, action, *data):
        """ handle spawned object death """
        if action == "die":
            self.spawned.remove(obj)
            obj.removeListener(self.onObjEvent)
            self.goSpawn()
    
    def remove(self):
        for to in self.timeouts:
            to.remove()
