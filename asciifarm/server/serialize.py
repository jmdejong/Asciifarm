
import importlib

modulePrefix = "asciifarm.server.components"

def getName(componentClass):
    module = componentClass.__module__
    if module.startswith(modulePrefix + "."):
        module = module.replace(modulePrefix + ".", ".", 1)
    return module + ":" + componentClass.__name__


def getClass(name):
    moduleName, className = name.split(":")
    module = importlib.import_module(moduleName, modulePrefix)
    componentClass = module.__getattribute__(className)
    return componentClass

def serialize(component):
    name = getName(type(component))
    return [name, component.toJSON()]

def unserialize(component):
    name, data = component
    return getClass(name).fromJSON(data)

def serializeEntity(obj):
    return obj.getComponent("serialize").serialize() if obj.hasComponent("serialize") else obj.toJSON()

