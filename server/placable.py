


class GameObject:
    
    char = ''
    size = 0
    attributes = {}
    
    def __init__(self, *args):
        pass
    
    def getChar(self):
        return self.char
    
    def place(self, ground):
        ground.addObj(self)
