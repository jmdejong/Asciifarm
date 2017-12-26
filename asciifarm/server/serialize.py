
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
    return [name, component.toJSON()]

def unserialize(component):
    name, data = component
    return getClass(component).fromJSON(data)

