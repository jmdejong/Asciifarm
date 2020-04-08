
import json
import os.path

from asciifarm.common import utils
from . import player


saveExt = ".save.json"

class PlayerLoader:
    
    def __init__(self, savePath):
        self.savePath = savePath
    
    def load(self, name, world):
        if not name:
            return None
        
        saved = None
        
        savePath = os.path.join(self.savePath, name + saveExt)
        try:
            with open(savePath, 'r') as f:
                saved = json.load(f)
        except OSError:
            saved = None
        p = player.Player.fromJSON(saved, world)
        return p
    
    def exists(self, name):
        savePath = os.path.join(self.savePath, name + saveExt)
        try:
            with open(savePath, 'r') as f:
                saved = json.load(f)
        except OSError:
            saved = None
        return saved is not None 
    
    def makeSaveDir(self):
        os.makedirs(self.savePath, exist_ok=True)
    
    
    def save(self, player):
        self.makeSaveDir()
        utils.writeFileSafe(os.path.join(self.savePath, player.getName() + saveExt), json.dumps(player.toJSON()))
    



