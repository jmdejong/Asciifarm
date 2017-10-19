


class Portal:
    
    def __init__(self, destRoom, destPos=None):
        self.destRoom = destRoom
        self.destPos = destPos
    
    def onEnter(self, obj):
        observable = obj.getComponent("observable")
        if observable:
            observable.trigger("changeroom", self.destRoom, self.destPos)

