


class RoomData:
    
    """ Instances of this class represents the data about the room that is available to the entities in the room and their components
    
    The Ground class does this as well, but Ground only gives local data, whereas this give data about the whole room.
    """
    
    def __init__(self, events=None):
        if events is None:
            events = []

        self.events = events
        self.targets = set()
        
        self.preservedObjects = set()
    
    
    def getEvent(self, name):
        return self.events[name]
    
    
    def addTarget(self, obj):
        self.targets.add(obj)
    
    def removeTarget(self, obj):
        self.targets.discard(obj)
    
    def getTargets(self):
        return frozenset(self.targets)
    
    def preserveObject(self, obj):
        self.preservedObjects.add(obj)
    
    def removePreserved(self, obj):
        self.preservedObjects.discard(obj)
    
    def getPreserved(self):
        return frozenset(self.preservedObjects)
    
