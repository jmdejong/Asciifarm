

import curses
from .fieldpad import FieldPad
from .infopad import InfoPad
from .healthpad import HealthPad
from .inventorypad import InventoryPad
from .screen import Screen


SIDEWIDTH = 20
HEALTHHEIGHT = 2
INVENTORYHEIGHT = 12


class Display:
    
    def __init__(self, stdscr, charMap, colours=False):
        
        self.screen = Screen(stdscr)
        self.fieldPad = FieldPad((64, 32), charMap.get("charwidth", 1), colours)
        self.characters = charMap["mapping"]
        self.defaultChar = charMap.get("default", "?")
        self.infoPad = InfoPad((100, 100))
        self.healthPad = HealthPad(20, ("@",39), ("-",23), colours)
        self.inventoryPad = InventoryPad("Inventory", 16)
        self.groundPad = InventoryPad("Ground", 8)
        self.lastinfostring = None
        self.colours = colours
        self.changed = False
        if colours:
            curses.use_default_colors()
            for i in range(0, min(256, curses.COLORS, curses.COLOR_PAIRS)):
                curses.init_pair(i, i%16, i//16)
            
    
    def resizeField(self, size):
        self.fieldPad.resize(*size)
    
    def drawFieldCells(self, cells):
        for cell in cells:
            (x, y), spriteName = cell
            sprite = self.getChar(spriteName)
            self.fieldPad.changeCell(x, y, *sprite)
        self.change()
    
    def setFieldCenter(self, pos):
        self.fieldPad.setCenter(pos)
    
    def setHealth(self, health, maxHealth):
        self.healthPad.setHealth(health, maxHealth)
        self.change()
    
    def showInfo(self, infostring):
        if infostring != self.lastinfostring:
            self.infoPad.showString(infostring)
            self.change()
            self.lastinfostring = infostring
    
    def setInventory(self, items):
        self.inventoryPad.setInventory(items)
        self.change()
    
    def setGround(self, items):
        self.groundPad.setInventory(items)
        self.change()
    
    def getChar(self, sprite):
        char = self.characters.get(sprite, self.defaultChar)
        if isinstance(char, str):
            return [char]
        return char
    
    def change(self):
        self.changed = True
    
    def update(self):
        if self.changed:
            fieldRight = min(self.fieldPad.getWidth(), self.screen.getWidth()-SIDEWIDTH-1)
            healthBottom = self.healthPad.getHeight()
            inventoryBottom = healthBottom + self.inventoryPad.getHeight()
            groundBottom = inventoryBottom + self.groundPad.getHeight()
            self.fieldPad.update(self, 0,0,fieldRight, min(self.fieldPad.getHeight(), self.screen.getHeight()))
            self.healthPad.update(self, fieldRight+1,0, self.screen.getWidth(), healthBottom)
            self.inventoryPad.update(self, fieldRight+1, healthBottom, self.screen.getWidth(), min(self.screen.getHeight(), inventoryBottom))
            self.groundPad.update(self, fieldRight+1, inventoryBottom, self.screen.getWidth(), min(self.screen.getHeight(), groundBottom))
            self.infoPad.update(self, fieldRight+1,groundBottom+1, self.screen.getWidth(), self.screen.getHeight())
            curses.doupdate()
        self.changed = False

