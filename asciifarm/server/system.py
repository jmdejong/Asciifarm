


def system(components, avoid=None):
    assert isinstance(components, list) or isinstance(components, tuple)
    def system_wrapper(func):
        def system_impl(roomData):
            entities = roomData.getEntities(components, avoid=avoid)
            for entity in entities:
                comps = [roomData.getComponent(entity, comp) for comp in components]
                func(entity, roomData, *comps)
        return system_impl
    return system_wrapper
