

class System:
    
    def __init__(self, components, code):
        self.components = components
        assert len(self.components) >= 1
        self.code = code
    
    def run(self, roomData):
        entities = set(roomData.dataComponents[self.components[0]])
        for component in self.components[1:]:
            entities &= roomData.dataComponents[component]
        for entity in entities:
            self.code(entity, roomData)

def system(components):
    def system_wrapper(func):
        return System(components, func)
    return system_wrapper
