
import json
import os.path

from asciifarm.common import utils
from . import player


saveExt = ".save.json"

class WorldLoader:
    """ A class for saving global world data
    
    Currently only saves the stepstamp
    """
    
    def __init__(self, savePath):
        self.savePath = savePath
    
    def load(self):
        
        saved = None
        
        savePath = os.path.join(self.savePath, "world" + saveExt)
        try:
            with open(savePath, 'r') as f:
                saved = json.load(f)
        except OSError:
            saved = None
        
        return saved
    
    
    def makeSaveDir(self):
        # todo
        # This method should ensure that the save directory exists
        pass
    
    
    def save(self, world):
        self.makeSaveDir()
        utils.writeFileSafe(os.path.join(self.savePath, "world" + saveExt), json.dumps({"steps": world.getStepStamp()}))
    



