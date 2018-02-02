
import json
import os.path

from asciifarm.common import utils
from . import room
from . import loader


saveExt = ".save.json"

class RoomLoader:
    
    def __init__(self, worldFile, savePath):
        with open(worldFile, 'r') as f:
            self.world = json.load(f)
        self.worldPath = os.path.dirname(worldFile)
        self.savePath = savePath
    
    
    def _loadRoom(self, roomPath):
        with open(roomPath) as roomFile:
            room = json.load(roomFile)
        for name, pos in room["places"].items():
            room["places"][name] = tuple(pos)
        return roomPath
    
    def load(self, name=None):
        if not name:
            name = self.world["begin"]
        base = None
        if name in self.world["rooms"]:
            try:
                base = self._loadRoom(os.path.join(self.worldPath, self.world["rooms"][name]))
            except OSError:
                return None
        
        saved = None
        
        savePath = os.path.join(self.savePath, name + saveExt)
        try:
            with open(savePath, 'r') as f:
                saved = json.load(f)
        except OSError:
            saved = None
        
        return room.Room(name, base, saved)
    
    def makeSaveDir(self):
        # todo
        # This method should ensure that the save directory exists
        pass
    
    
    def save(self, room):
        self.makeSaveDir()
        utils.writeFileSafe(os.path.join(self.savePath, room.getName() + saveExt), json.dumps(room.getPreserved()))
    



