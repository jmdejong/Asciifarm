


class Portal:
    
    def __init__(self, destRoom, destPos=None):
        self.destRoom = destRoom
        self.destPos = destPos
    
    def attach(self, obj, roomData):
        obj.addListener(self.onObjEvent)
        
    
    def onObjEvent(self, owner, action, obj=None, *data):
        if action == "objectenter":
            obj.trigger("changeroom", self.destRoom, self.destPos)

