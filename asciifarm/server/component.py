


class Component:
    
    
    def attach(self, obj, roomData):
        pass
    
    
    def remove(self):
        pass
    
    def toJSON(self):
        return None
    
    @classmethod
    def fromJSON(cls, data=None):
        if data == None:
            return cls()
        return cls(**data)
