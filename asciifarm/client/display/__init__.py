

import curses
from .fieldpad import FieldPad
from .infopad import InfoPad
from .healthpad import HealthPad
from .inventorypad import InventoryPad
from .screen import Screen
from .colours import Colours
from .messagepad import MessagePad


SIDEWIDTH = 20


class Display:
    
    def __init__(self, stdscr, charMap, colours=False):
        
        if colours:
            self.colours = Colours()
        else:
                self.colours = None
        self.screen = Screen(self, stdscr)
        self.fieldPad = FieldPad((1, 1), charMap.get("charwidth", 1), self.colours)
        self.characters = charMap["mapping"]
        self.defaultChar = charMap.get("default", "?")
        self.infoPad = InfoPad()
        self.healthPad = HealthPad(
                    charMap.get("healthfull", ("@",7, 2)),
                    charMap.get("healthempty", ("-",7, 1)),
                    self.colours)
        self.inventoryPad = InventoryPad("Inventory")
        self.groundPad = InventoryPad("Ground")
        self.lastinfostring = None
        self.changed = False
        self.messagePad = messagepad.MessagePad()
        
        self.screen.update(True)
            
    
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
        
    def addMessage(self, message):
        self.messagePad.addMessage(message)
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
            self.screen.update()
            
        self.changed = False

