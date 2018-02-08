
import heapq
import itertools
counter = itertools.count()     # unique sequence count


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
        
        self.stepStamp = 0
        
        self.alarms = [] # treat as priority queue
    
    
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
    
    def setAlarm(self, stamp, callback):
        
        count = next(counter) # tiebreaker for when stamps are equal
        # see: https://docs.python.org/3/library/heapq.html#priority-queue-implementation-notes
        heapq.heappush(self.alarms, (stamp, count, callback))
    
    def triggerAlarms(self):
        while self.alarms and self.alarms[0][0] <= self.stepStamp:
            _plannedTime, _count, callback = heapq.heappop(self.alarms)
            callback()
    
    def setStamp(self, stamp):
        self.stepStamp = stamp
    
    def getStamp(self):
        return self.stepStamp
    
