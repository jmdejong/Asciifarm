
import importlib

def getName(componentClass):
    return componentClass.__module__ + ":" + componentClass.__name__


def getClass(name):
    moduleName, className = name.split(":")
    module = importlib.import_module(moduleName)
    componentClass = module.__getattribute__(className)
    return componentClass

def serialize(component):
    module, name = getName(type(component))
    if not hasattr(component, "toJSON"):
        return name
    return [name, component.toJSON()]

def unserialize(component):
    if isinstance(component, str):
        return getClass(component)()
    if isinstance(component, list):
        name, data = component
        return getClass(component).fromJSON(data)
    raise Exception("Invalid component type: "+component)

