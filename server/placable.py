


class GameObject:
    
    char = ''
    size = 0
    attributes = {}
    
    def __init__(self, *args, **kwargs):
        pass
    
    def getChar(self):
        return self.char
    
    def place(self, ground):
        ground.addObj(self)
    
    def getInteractions(self):
        return {}
    
    def exists(self):
        return True
