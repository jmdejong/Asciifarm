
from . import serialize
import collections
from .datacomponents import Events, Remove

class Entity:
    """ Attempt to implement an entity component system

    This is the base object
    Components are given on construction.
    Once a component is added to the object the attach method will be called on the component (if it has one).
    The attach method is used to pass the entity and room events to the component.
    When the entity is removed, all components will have their remove method called if they have one.
    Remove methods are for cleanup, like unsubscribing from events.
    """
    
    def __init__(self, sprite=' ', height=0, name=None, components=None, flags=None, dataComponents=None):
        if components is None:
            components = {}
        if flags is None:
            flags = set()
        self.sprite = sprite # the name of the image to display for this entity
        self.height = height # if multiple objects are on a square, the tallest one is drawn
        self.name = name if name else sprite # human readable name/description
        self.components = components
        self.flags = set(flags)
        self.ground = None
        self.roomData = None
        if dataComponents is None:
            dataComponents = []
        self.dataComponents = {type(comp): comp for comp in dataComponents}
        
        self.listeners = collections.defaultdict(dict)
        
        for component in self.components.values():
            component.attach(self)
        
        
    
    def construct(self, roomData, preserve=False, stamp=None):
        self.roomData = roomData
        if preserve:
            roomData.preserveObject(self)
            self._preserve()
        self.roomData.addObj(self)
        if stamp is None:
            stamp = roomData.getStamp()
        self.trigger("roomjoin", roomData, stamp)
    
    def hasComponent(self, name):
        return name in self.components
    
    def getComponent(self, name):
        return self.components.get(name, None)
    
    def listComponents(self):
        return list(self.components.keys())
    
    def getDataComponent(self, component):
        return self.roomData.getComponent(self, component)
    
    def place(self, ground):
        if self.ground:
            self.ground.removeObj(self)
        self.ground = ground
        ground.addObj(self)
    
    def remove(self):
        self.trigger("remove")
        self.roomData.addComponent(self, Remove)
        
    
    def doRemove(self):
        self.roomData.removeObj(self)
        if self.isPreserved():
            self.roomData.removePreserved(self)
        for component in self.components.values():
            component.remove()
        if self.ground:
            self.ground.removeObj(self)
            self.ground = None
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
    
    def getFlags(self):
        return self.flags
    
    def _preserve(self):
        self.flags.add("preserve")
    
    def isPreserved(self):
        return "preserve" in self.flags
    
    def toJSON(self):
        return {
            "sprite": self.sprite,
            "name": self.name,
            "height": self.height,
            "flags": list(self.flags),
            "components": {
                name: serialize.serialize(comp)
                for name, comp in self.components.items()
            }
        }
    
    def serialize(self):
        if "serialize" not in self.components:
            return self.toJSON()
        return self.components["serialize"].serialize()
    
    @classmethod
    def fromJSON(cls, data):
        if data is None:
            return None
        return cls(
            sprite = data["sprite"],
            name = data["name"],
            height = data["height"],
            flags = data["flags"],
            components = {
                name: serialize.unserialize(comp)
                for name, comp in data["components"].items()
            }
        )
    
    def getRoomData(self):
        return self.roomData
