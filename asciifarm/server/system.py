

class _System:
    
    def __init__(self, components, code, combinator="intersect"):
        self.components = components
        assert len(self.components) >= 1
        self.code = code
        self.combinator = combinator
        
    
    def run(self, roomData):
        entities = set(roomData.dataComponents[self.components[0]])
        if self.combinator == "intersect":
            for component in self.components[1:]:
                entities &= roomData.dataComponents[component]
        elif self.combinator == "union":
            for component in self.components[1:]:
                entities |= roomData.dataComponents[component]
        for entity in entities:
            components = [entity.getDataComponent(comp) for comp in self.components]
            self.code(entity, roomData, *components)

def System(components, combinator="intersect"):
    def system_wrapper(func):
        return _System(components, func, combinator)
    return system_wrapper
