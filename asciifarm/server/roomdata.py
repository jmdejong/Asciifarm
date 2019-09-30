
import heapq
import itertools
import collections
counter = itertools.count()     # unique sequence count

from .systems.fight import fight
from .systems.attacked import attacked
from .systems.heal import heal
from .systems.move import move
from .systems.controlai import controlai
from .systems.controlinput import control

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
        
        self.objects = set()
        
        self.components = collections.defaultdict(set) # type: {str: set(Entity)}
        self.dataComponents = collections.defaultdict(set) # type: {str: set(Entity)}
    
    def addObj(self, obj):
        
        self.objects.add(obj)
        for component in obj.listComponents():
            self.components[component].add(obj)
        for compt in obj.dataComponents:
            self.dataComponents[compt].add(obj)
    
    def removeObj(self, obj):
        self.objects.remove(obj)
        for component in obj.listComponents():
            self.components[component].remove(obj)
        for compt in obj.dataComponents:
            if obj not in self.dataComponents[compt]:
                print(compt, obj.toJSON())
            self.dataComponents[compt].remove(obj)
    
    def addComponent(self, obj, component):
        if isinstance(component, type):
            component = component()
        compt = type(component)
        self.dataComponents[compt].add(obj)
        obj.dataComponents[compt] = component
    
    def removeComponent(self, obj, compt):
        if obj not in self.dataComponents[compt]:
            print(compt, obj.toJSON())
        self.dataComponents[compt].remove(obj)
        obj.dataComponents.pop(compt)
        
        
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
    
