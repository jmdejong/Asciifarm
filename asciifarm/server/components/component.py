


class Component:
    
    
    def attach(self, obj):
        pass
    
    
    def remove(self):
        pass
    
    def toJSON(self):
        return None
    
    @classmethod
    def fromJSON(cls, data=None):
        if data is None:
            return cls()
        return cls(**data)
