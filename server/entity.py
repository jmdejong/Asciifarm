

# Attempt to implement an entity component system
# This is the base object
# Contrary to my earlier attempts to implement this (in other projects),
# this class is not as small as possible
# Hopefully this will make the code simpler

# This page explains the composition patter that I'm trying to use here:
# http://www.roguebasin.com/index.php?title=Complete_Roguelike_Tutorial,_using_python%2Blibtcod,_part_6
# main difference: I don't give entities an attribute for each component type, but store the components in a dict instead


class Entity:
    
    
    def __init__(self, roomEvents, sprite=' ', solid=False, height=0, name=None, components={}):
        self.sprite = sprite # the name of the image to display for this entity
        self.solid = solid
        self.height = height # if multiple objects are on a square, the tallest one is drawn
        self.name = name if name else sprite # human readable name/description
        self.components = components
        
        for component in components.values():
            if hasattr(component, "attach"):
                component.attach(self, roomEvents)
        
        self.ground = None
        pass
    
    def hasComponent(self, name):
        return name in self.components
    
    def getComponent(self, name):
        return self.components.get(name, None)
    
    
    def place(self, ground):
        if self.ground:
            self.ground.removeObj(self)
        ground.addObj(self)
        self.ground = ground
    
    def remove(self):
        if self.ground:
            self.ground.removeObj(self)
            self.ground = None
        
        for component in self.components.values():
            if hasattr(component, "remove"):
                component.remove()
    
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
    
    def isSolid(self):
        return self.solid
    
    def setName(self, name):
        self.name = name
    
    def setSprite(self, sprite):
        self.sprite = sprite
    
    def setHeight(self, height):
        self.height = height
    
    def setSolid(self, solid):
        self.solid = solid
    
    
