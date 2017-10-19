


class GameObject:
    
    char = ''
    size = 0
    attributes = {}
    ground = None
    
    def __init__(self, *args, **kwargs):
        pass
    
    def getChar(self):
        return self.char
    
    def getInteractions(self):
        return {}
    
    def inRoom(self):
        return self.ground != None
    
    def place(self, ground):
        if self.ground:
            self.ground.removeObj(self)
        ground.addObj(self)
        self.ground = ground
    
    def remove(self):
        if self.ground:
            self.ground.removeObj(self)
            self.ground = None
    
    def isSolid(self):
        return "solid" in self.attributes
    
    def isTakable(self): # temp hack until entities replaces gameobjects
        return "takable" in self.attributes
    
    def getGround(self):
        return self.ground
    
    def getHeight(self):
        return self.size
    
