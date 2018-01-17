
import string

from . import loader
from .room import Room
import os.path

class WorldTemplate:
    
    
    def __init__(self, world=None, worldDir=None, loadDir=None):
        
        self.world = world
        self.prefabs = {}
    
    
    def addPrefabs(self, prefabs):
        for name, data in prefabs.items():
            self.addPrefab(name, data)
    
    def addPrefab(self, name, data):
        self.prefabs[name] = data
    
    def loadRoom(self, name):
        if not name:
            return None
        if name[0] in string.ascii_letters:
            base = loader.loadRoom(os.path.join(worldDir, name + ".json"))
    
    def getTemplate(self, name):
        if name in self.prefabs:
            return self.prefabs[name]
        
        return None
    
    def getRoom(self, name):
        template = self.getTemplate(name)
        if not template:
            return None
        return Room(name, template)
