
from .conversions import convert

class Template:
    
    def __init__(self, name, *args, **kwargs):
        
        self.name = name
        self.args = list(args)
        self.kwargs = dict(kwargs)
    
    def toJSON(self):
        if self.args or self.kwargs:
            return {
                "type": self.name,
                "args": self.args,
                "kwargs": self.kwargs
            }
        else:
            return self.name
    
    def __repr__(self):
        a = [self.name]
        for arg in self.args:
            a.append(repr(arg))
        for key, value in self.kwargs.items():
            a.append(key + "=" + repr(value))
        return "Template({})".format(", ".join(a))
    
    @classmethod
    def fromJSON(cls, value):
        if isinstance(value, str):
            return cls(value)
        if isinstance(value, dict) and "type" in value:
            return cls(value["type"], *value.get("args", []), **value.get("kwargs", {}))
        if isinstance(value, list):
            if len(value) == 1:
                return cls(value[0])
            if len(value) == 2:
                return cls(value[0], *value[1])
            if len(value) == 3:
                return cls(value[0], *value[1], value[2])
        if isinstance(value, dict) and "components" in value:
            return Template.fromJSON(convert(value))
            
        raise ValueError(value)
