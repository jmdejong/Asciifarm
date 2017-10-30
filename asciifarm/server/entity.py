from . import event


class Entity:
    """ Attempt to implement an entity component system

    This is the base object
    Components are given on construction.
    Once a component is added to the object the attach method will be called on the component (if it has one).
    The attach method is used to pass the entity and room events to the component.
    When the entity is removed, all components will have their remove method called if they have one.
    Remove methods are for cleanup, like unsubscribing from events.
    """
    
    def __init__(self, sprite=' ', height=0, name=None, components={}, flags=set()):
        self.sprite = sprite # the name of the image to display for this entity
        self.height = height # if multiple objects are on a square, the tallest one is drawn
        self.name = name if name else sprite # human readable name/description
        self.components = components
        self.observable = event.Event()
        self.flags = frozenset(flags)
        
        self.ground = None
        self.roomData = None
        pass
    
    def construct(self, roomData):
        self.roomData = roomData
        for component in self.components.values():
            if hasattr(component, "attach"):
                component.attach(self, roomData)
    
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
        for component in self.components.values():
            if hasattr(component, "remove"):
                component.remove()
        self.trigger("remove")
        self.roomData = None
    
    def addListener(self, callback, key=None):
        self.observable.addListener(callback, key)
    
    def removeListener(self, key):
        self.observable.removeListener(key)
    
    def trigger(self, *args):
        self.observable.trigger(self, *args)
    
    def getSprite(self):
        return self.sprite
    
    def getName(self):
        return self.name
    
    def getHeight(self):
        return self.height
    
    def inRoom(self):
        return self.ground != None
    
    def getGround(self):
        return self.ground
    
    def getNearObjects(self):
        objects = set(self.ground.getObjs())
        objects.discard(self)
        return objects
    
    def getFlags(self):
        return self.flags
    