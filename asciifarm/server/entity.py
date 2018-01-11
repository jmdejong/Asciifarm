#from . import event
from . import serialize
from .eventtarget import EventTarget


class Entity:
    """ Attempt to implement an entity component system

    This is the base object
    Components are given on construction.
    Once a component is added to the object the attach method will be called on the component (if it has one).
    The attach method is used to pass the entity and room events to the component.
    When the entity is removed, all components will have their remove method called if they have one.
    Remove methods are for cleanup, like unsubscribing from events.
    """
    
    def __init__(self, sprite=' ', height=0, name=None, components=None, flags=None):
        if components is None:
            components = {}
        if flags is None:
            flags = set()
        self.sprite = sprite # the name of the image to display for this entity
        self.height = height # if multiple objects are on a square, the tallest one is drawn
        self.name = name if name else sprite # human readable name/description
        self.components = components
        self.observable = EventTarget()
        self.flags = set(flags)
        self.ground = None
        self.roomData = None
        for component in self.components.values():
            component.attach(self)
        
    
    def construct(self, roomData, preserve=False):
        self.roomData = roomData
        if preserve:
            roomData.preserveObject(self)
            self._preserve()
        self.trigger("roomjoin", roomData)
    
    def hasComponent(self, name):
        return name in self.components
    
    def getComponent(self, name):
        return self.components.get(name, None)
    
    
    def place(self, ground):
        if self.ground:
            self.ground.removeObj(self)
        self.ground = ground
        ground.addObj(self)
    
    def remove(self):
        if self.ground:
            self.ground.removeObj(self)
            self.ground = None
        if self.isPreserved():
            self.roomData.removePreserved(self)
        for component in self.components.values():
            component.remove()
        self.trigger("remove")
        self.roomData = None
    
    def addListener(self, event, callback, key=None):
        self.observable.addListener(event, callback, key)
    
    def removeListener(self, event, key):
        self.observable.removeListener(event, key)
    
    def trigger(self, event, *args, **kwargs):
        self.observable.trigger(event, self, *args, **kwargs)
    
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
    
