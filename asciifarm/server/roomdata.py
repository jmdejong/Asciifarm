
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

from .datacomponents import DC


class RoomData:
    
    """ Instances of this class represents the data about the room that is available to the entities in the room and their components
    
    The Ground class does this as well, but Ground only gives local data, whereas this give data about the whole room.
    """
    
    def __init__(self):
        self.targets = set()
        
        self.preservedObjects = set()
        
        self.stepStamp = 0
        
        self.alarms = [] # treat as priority queue
        self.postponed = []
        
        self.objects = set()
        
        self.sounds = []
        
        self.dataComponents = collections.defaultdict(set) # type: {str: set(Entity)}
    
    def addObj(self, obj):
        
        self.objects.add(obj)
        for compt in obj.dataComponents:
            self.dataComponents[compt].add(obj)
    
    def removeObj(self, obj):
        self.objects.remove(obj)
        for compt in obj.dataComponents:
            if obj not in self.dataComponents[compt]:
                print(compt, obj.toJSON())
            self.dataComponents[compt].remove(obj)
    
    
    def addComponent(self, obj, component):
        if isinstance(component, type):
            compt = component
            component = component()
        else:
            compt = type(component)
        self.dataComponents[compt].add(obj)
        if isinstance(component, DC) and component.allowMultiple:
            if compt not in obj.dataComponents:
                obj.dataComponents[compt] = []
            obj.dataComponents[compt].append(component)
        else:
            obj.dataComponents[compt] = component
    
    def removeComponent(self, obj, component, gone_ok=False):
        if isinstance(component, type):
            compt = component
            component = self.getComponent(obj, compt)
        else:
            compt = type(component)
        if component is None:
            if gone_ok:
                return
            else:
                raise KeyError("object {} has no component {}".format(str(object), str(component)))
        if isinstance(component, DC) and component.allowMultiple:
            l = obj.dataComponents[compt]
            l.remove(component)
            if not l:
                self.dataComponents[compt].remove(l)
        else:
            self.dataComponents[compt].remove(obj)
            obj.dataComponents.pop(compt)
    
    def clearComponent(self, compt):
        for entity in self.dataComponents[compt]:
            del entity.dataComponents[compt]
        self.dataComponents[compt] = set()
    
    def getComponent(self, obj, component):
        return obj.dataComponents.get(component)
    
    def getEntities(self, compts, combinator="intersect", avoid=None):
        
        entities = set(self.dataComponents[compts[0]])
        if combinator == "intersect":
            for compt in compts[1:]:
                entities &= self.dataComponents[compt]
        elif combinator == "union":
            for compt in compts[1:]:
                entities |= self.dataComponents[compt]
        if avoid is not None:
            for compt in avoid:
                entities -= self.dataComponents[compt]
        return entities
    
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
        while self.postponed and self.postponed[0][0] <= self.stepStamp:
            _plannedTime, _count, obj, components = heapq.heappop(self.postponed)
            if obj not in self.objects:
                return
            for component in components:
                self.addComponent(obj, component)
        while self.alarms and self.alarms[0][0] <= self.stepStamp:
            _plannedTime, _count, callback = heapq.heappop(self.alarms)
            callback()
    
    def setStamp(self, stamp):
        self.stepStamp = stamp
    
    def getStamp(self):
        return self.stepStamp
    
    def makeSound(self, source, text):
        self.sounds.append((source, text))
    
    def postpone(self, stamp, obj, *components):
        count = next(counter) # tiebreaker for when stamps are equal
        # see: https://docs.python.org/3/library/heapq.html#priority-queue-implementation-notes
        heapq.heappush(self.postponed, (stamp, count, obj, list(components)))
    
