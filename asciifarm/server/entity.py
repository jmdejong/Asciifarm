
from . import serialize
import collections
from .datacomponents import Events, Remove, Serialise, Preserve

class Entity:
    """ Attempt to implement an entity component system

    This is the base object
    Components are given on construction.
    Once a component is added to the object the attach method will be called on the component (if it has one).
    The attach method is used to pass the entity and room events to the component.
    When the entity is removed, all components will have their remove method called if they have one.
    Remove methods are for cleanup, like unsubscribing from events.
    """
    
    def __init__(self, sprite=' ', height=0, name=None, dataComponents=None):
        self.sprite = sprite # the name of the image to display for this entity
        self.height = height # if multiple objects are on a square, the tallest one is drawn
        self.name = name if name else sprite # human readable name/description
        self.ground = None
        self.roomData = None
        if dataComponents is None:
            dataComponents = []
        self.dataComponents = {}
        for component in dataComponents:
            if isinstance(component, type):
                compt = component
                component = component()
            else:
                compt = type(component)
            self.dataComponents[compt] = component
        
        self.listeners = collections.defaultdict(dict)
        
        
        
    
    def construct(self, roomData, preserve=False, stamp=None):
        self.roomData = roomData
        if preserve:
            roomData.preserveObject(self)
        self.roomData.addObj(self)
        if stamp is None:
            stamp = roomData.getStamp()
        self.trigger("roomjoin", roomData, stamp)
    
    def getDataComponent(self, component):
        return self.roomData.getComponent(self, component)
    
    def place(self, ground):
        if self.ground:
            self.ground.removeObj(self)
        self.ground = ground
        ground.addObj(self)
    
    def unPlace(self):
        if self.ground:
            self.ground.removeObj(self)
            self.ground = None
        
    
    def remove(self):
        self.trigger("remove")
        self.roomData.addComponent(self, Remove)
        
    
    def doRemove(self):
        self.roomData.removeObj(self)
        self.unPlace()
        self.roomData = None
    
    def addListener(self, event, callback, key=None):
        if key is None:
            key = callback
        self.listeners[event][key] = callback
    
    def removeListener(self, event, key):
        self.listeners[event].pop(key)
    
    def trigger(self, event, *args, **kwargs):
        messages = self.getDataComponent(Events)
        if messages is None:
            messages = Events()
            self.roomData.addComponent(self, messages)
        messages.add((event, list(args), dict(kwargs)))
    
    def getSprite(self):
        return self.sprite
    
    def getName(self):
        return self.name
    
    def getHeight(self):
        return self.height
    
    def inRoom(self):
        return self.ground is not None

    def getGround(self):
        return self.ground
    
    def getNearObjects(self):
        return [obj for obj in self.ground.getObjs() if obj != self]
    
    def serialize(self):
        if Serialise in self.dataComponents:
            return self.dataComponents[Serialise].serialise(self, self.roomData)
        else:
            return None
    
    def getRoomData(self):
        return self.roomData
