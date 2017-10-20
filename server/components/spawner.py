
import timeout
import gameobjects

class Spawner:
    
    def __init__(self, objectType, amount=1, respawnDelay=1, objectArgs=[], objectKwargs={}):
        self.objectType = objectType
        self.amount = amount
        self.respawnDelay = respawnDelay # currently ignored
        self.spawned = set()
        self.objectArgs = objectArgs
        self.objectKwargs = objectKwargs
    
    def attach(self, obj, events):
        
        self.owner = obj
        self.roomEvents = events
        self.updateEvent = events["update"]
        self.timeout = timeout.Timeout(events["update"], self.respawnDelay, callback=self.spawn)
        
        for i in range(self.amount):
            self.goSpawn()
    
    def goSpawn(self): # todo: remove timeouts when spawner gets removed
        timeout.Timeout(self.updateEvent, self.respawnDelay, callback=self.spawn).timeout()
    
    def spawn(self):
        obj = gameobjects.makeEntity(self.objectType, self.roomEvents, *self.objectArgs, **self.objectKwargs)
        obj.place(self.owner.getGround())
        self.spawned.add(obj)
        obj.addListener(self.onObjEvent)
        print("{} spawned a {}".format(self.owner.getName(), self.objectType))
    
    
    def onObjEvent(self, obj, action, *data):
        """ handle spawned object death """
        if action == "die":
            self.spawned.remove(obj)
            obj.removeListener(self.onObjEvent)
            self.goSpawn()
    
