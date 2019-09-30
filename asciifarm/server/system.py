

class _System:
    
    def __init__(self, components, code):
        self.components = components
        assert len(self.components) >= 1
        self.code = code
    
    def run(self, roomData):
        entities = set(roomData.dataComponents[self.components[0]])
        for component in self.components[1:]:
            entities &= roomData.dataComponents[component]
        for entity in entities:
            components = [entity.getDataComponent(comp) for comp in self.components]
            self.code(entity, roomData, *components)

def System(*components):
    def system_wrapper(func):
        return _System(list(components), func)
    return system_wrapper
