

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
        self.screen = Screen(stdscr)
        self.fieldPad = FieldPad((1, 1), charMap.get("charwidth", 1), self.colours)
        self.characters = charMap["mapping"]
        self.defaultChar = charMap.get("default", "?")
        self.infoPad = InfoPad((100, 100))
        self.healthPad = HealthPad(20, 
                    charMap.get("healthfull", ("@",7, 2)),
                    charMap.get("healthempty", ("-",7, 1)),
                    self.colours)
        self.inventoryPad = InventoryPad("Inventory", 10)
        self.groundPad = InventoryPad("Ground", 5)
        self.lastinfostring = None
        self.changed = False
        self.messagePad = messagepad.MessagePad(5)
            
    
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
            fieldRight = min(self.fieldPad.getWidth(), self.screen.getWidth()-SIDEWIDTH-1)
            fieldBottom = min(self.fieldPad.getHeight(), self.screen.getHeight()-self.messagePad.getHeight())
            healthBottom = self.healthPad.getHeight()
            groundBottom = healthBottom + self.groundPad.getHeight()
            inventoryBottom = groundBottom + self.inventoryPad.getHeight()
            self.fieldPad.update(self, 0,0,fieldRight, fieldBottom)
            self.messagePad.update(self, 0,fieldBottom, fieldRight, min(self.screen.getHeight(), fieldBottom+self.messagePad.getHeight()))
            self.healthPad.update(self, fieldRight+1,0, self.screen.getWidth(), healthBottom)
            self.groundPad.update(self, fieldRight+1, healthBottom, self.screen.getWidth(), min(self.screen.getHeight(), groundBottom))
            self.inventoryPad.update(self, fieldRight+1, groundBottom, self.screen.getWidth(), min(self.screen.getHeight(), inventoryBottom))
            self.infoPad.update(self, fieldRight+1,inventoryBottom+1, self.screen.getWidth(), self.screen.getHeight())
            
            curses.doupdate()
        self.changed = False

