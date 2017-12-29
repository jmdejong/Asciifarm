

import curses
from .fieldpad import FieldPad
from .infopad import InfoPad
from .healthpad import HealthPad
from .inventorypad import InventoryPad
from .screen import Screen
from .colours import Colours
from .messagepad import MessagePad
from .textinput import TextInput


SIDEWIDTH = 20


class Display:
    
    def __init__(self, stdscr, charMap, colours=False):
        
        if colours:
            self.colours = Colours()
        else:
                self.colours = None
        self.characters = charMap["mapping"]
        self.defaultChar = charMap.get("default", "?")
        self.screen = Screen(self, stdscr)
        
        def setwin(pad, winname):
            pad.setWin(self.screen.getWin(winname))
        
        self.fieldPad = FieldPad((1, 1), charMap.get("charwidth", 1), self.colours)
        setwin(self.fieldPad, "field")
        self.infoPad = InfoPad()
        setwin(self.infoPad, "info")
        self.healthPad = HealthPad(
                    charMap.get("healthfull", ("@",7, 2)),
                    charMap.get("healthempty", ("-",7, 1)),
                    self.colours)
        setwin(self.healthPad, "health")
        self.inventoryPad = InventoryPad("Inventory")
        setwin(self.inventoryPad, "inventory")
        self.groundPad = InventoryPad("Ground")
        setwin(self.groundPad, "ground")
        self.messagePad = MessagePad()
        setwin(self.messagePad, "msg")
        self.textInput = TextInput()
        setwin(self.textInput, "textinput")
        
        self.lastinfostring = None
        
        
        self.widgets = {
            "field": self.fieldPad,
            "info": self.infoPad,
            "health": self.healthPad,
            "inventory": self.inventoryPad,
            "ground": self.groundPad,
            "msg": self.messagePad,
            "textinput": self.textInput
        }
        #self.changed = False
        
        self.update()
    
    def getWidget(self, name):
        return self.widgets.get(name, None)
    
    def resizeField(self, size):
        self.fieldPad.resize(*size)
    
    def drawFieldCells(self, cells):
        for cell in cells:
            (x, y), spriteName = cell
            sprite = self.getChar(spriteName)
            self.fieldPad.changeCell(x, y, *sprite)
        #self.change()
    
    def setFieldCenter(self, pos):
        self.fieldPad.setCenter(pos)
    
    def setHealth(self, health, maxHealth):
        self.healthPad.setHealth(health, maxHealth)
        #self.change()
    
    def showInfo(self, infostring):
        if infostring != self.lastinfostring:
            self.infoPad.showString(infostring)
            #self.change()
            self.lastinfostring = infostring
    
    def setInventory(self, items):
        self.inventoryPad.setInventory(items)
        #self.change()
    
    def setGround(self, items):
        self.groundPad.setInventory(items)
        #self.change()
    
    def getSelector(self, name):
        widget = self.getWidget(name)
        if not widget or not hasattr(widget, "getSelector"):
            return None
        return widget.getSelector()
        
    
    def addMessage(self, message):
        self.messagePad.addMessage(message)
        #self.change()
    
    def getChar(self, sprite):
        """This returns the character belonging to some spritename. This does not read a character"""
        char = self.characters.get(sprite, self.defaultChar)
        if isinstance(char, str):
            return [char]
        return char
    
    def getString(self):
        """This does actually read input"""
        return self.textInput.getString()
    
    #def change(self):
        #self.changed = True
    
    def update(self, force=False):
        #if not self.changed and not force:
            #return
        
        self.fieldPad.update(force)
        self.messagePad.update(force)
        self.healthPad.update(force)
        self.groundPad.update(force)
        self.inventoryPad.update(force)
        self.infoPad.update(force)
        
        self.textInput.update(force)
        
        self.screen.update()
            
        #self.changed = False

