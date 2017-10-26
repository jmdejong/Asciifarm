

import curses
from .fieldpad import FieldPad
from .infopad import InfoPad
from .healthpad import HealthPad

class Display:
    
    def __init__(self, screen, charMap):
        
        self.screen = screen
        self.fieldPad = FieldPad((64, 32), charMap.get("charwidth", 1))
        self.characters = charMap["mapping"]
        self.defaultChar = charMap.get("default", "?")
        self.infoPad = InfoPad((100, 100))
        self.healthPad = HealthPad((20, 1))
        self.lastinfostring = None
    
    def resizeField(self, size):
        self.fieldPad.resize(*size)
    
    def drawFieldCells(self, cells):
        for cell in cells:
            (x, y), spriteName = cell
            sprite = self.getChar(spriteName)
            self.fieldPad.changeCell(x, y, sprite)
        self.screen.change()
    
    def showHealth(self, health, maxHealth):
        self.healthPad.setHealth(health, maxHealth)
        self.screen.change()
    
    def showInfo(self, infostring):
        if infostring != self.lastinfostring:
            self.infoPad.showString(infostring)
            self.screen.change()
            self.lastinfostring = infostring
    
    def getChar(self, sprite):
        char = self.characters.get(sprite, self.defaultChar)
        if isinstance(char, str):
            return char
        return char[0]
    
    def update(self):
        self.screen.update(self.fieldPad, self.infoPad, self.healthPad)
    

