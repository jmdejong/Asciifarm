


class Portal:
    
    def __init__(self, destRoom, destPos=None):
        self.destRoom = destRoom
        self.destPos = destPos
    
    def onEnter(self, obj):
        
        obj.trigger("changeroom", self.destRoom, self.destPos)

