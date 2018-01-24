

from .component import Component

class StaticSerializer(Component):
    """ This class is for static serialization.
    
    If an entity has this component then the serialization will be the argument passed to the constructor instead of the toJSON of the entity and its components.
    This is useful for objects that hold no state and are not unique.
    """
    
    def __init__(self, data, *args, **kwargs):
        if isinstance(data, str):
            self.data = {"type": data, "args": args, "kwargs": kwargs}
        else:
            self.data = data
    
    def serialize(self):
        return self.data
