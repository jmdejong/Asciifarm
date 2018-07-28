

class Option:
    
    def __init__(self, action, name=None, description=None):
        self.action = action
        if name is None:
            self.name = id(self)
        else:
            self.name = name
        if description is None:
            self.description = self.name
        else:
            self.description = description
    
    def act(self, obj):
        self.action(obj)
