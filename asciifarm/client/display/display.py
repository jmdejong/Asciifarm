

import curses
from .fieldpad import FieldPad
from .infopad import InfoPad
from .healthpad import HealthPad
from .inventorypad import InventoryPad
from .screen import Screen
from .colours import Colours
from .messagepad import MessagePad
from .textinput import TextInput
from .widget import Widget

from asciifarm.common.utils import get


SIDEWIDTH = 20


class Display:
    
    def __init__(self, stdscr, charMap, colours=False):
        
        if colours:
            self.colours = Colours()
        else:
                self.colours = None
        self.characters = {}
        for name, sprite in charMap["mapping"].items():
            if isinstance(sprite, str):
                self.characters[name] = (sprite, None, None)
                continue
            char = get(sprite, 0, " ")
            fg = get(sprite, 1)
            bg = get(sprite, 2)
            self.characters[name] = (char, fg, bg)
        self.defaultChar = charMap.get("default", "?")
        self.screen = Screen(self, stdscr)
        
        self.widgets = {}
        
        def setwin(pad, widgetName, winname=None):
            if not winname:
                winname = widgetName
            widget = Widget(pad)
            self.widgets[widgetName] = widget
            widget.setWin(self.screen.getWin(winname))
        
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
        self.equipment = InventoryPad("Equipment")
        setwin(self.equipment, "equipment")
        self.messagePad = MessagePad()
        setwin(self.messagePad, "msg")
        self.textInput = TextInput()
        setwin(self.textInput, "textinput")
        
        self.lastinfostring = None
        
        #self.changed = False
        
        self.update()
    
    def getWidget(self, name):
        if name in self.widgets:
            return self.widgets[name].getImpl()
        else:
            return None
    
    def resizeField(self, size):
        self.fieldPad.resize(*size)
    
    def drawFieldCells(self, cells):
        for cell in cells:
            (x, y), spriteNames = cell
            sprites = [self.getChar(spriteName) for spriteName in spriteNames]
            if not len(sprites):
                sprites = [self.getChar(" ")]
            self.fieldPad.changeCell(x, y, sprites)
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
    
    def setEquipment(self, slots):
        self.equipment.setInventory(
            sorted([
                slot + ": " + (item if item else "")
                for slot, item in slots.items()
            ])
        )
    
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
        return self.characters.get(sprite, self.defaultChar)
    
    def getString(self):
        """This does actually read input"""
        return self.textInput.getString()
    
    #def change(self):
        #self.changed = True
    
    def update(self, force=False):
        #if not self.changed and not force:
            #return
        for widget in self.widgets.values():
            if force:
                widget.change()
            widget.update()
        
        self.screen.update()
            
        #self.changed = False

