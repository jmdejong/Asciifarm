


def system(components):
    def system_wrapper(func):
        def system_impl(roomData):
            entities = roomData.getEntities(components)
            for entity in entities:
                comps = [entity.getDataComponent(comp) for comp in components]
                func(entity, roomData, *comps)
        return system_impl
    return system_wrapper
