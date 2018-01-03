

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
        self.screen = Screen(self, stdscr, self.colours)
        
        self.widgets = {}
        
        self.addWidget(FieldPad((1, 1), charMap.get("charwidth", 1), self.colours), "field")
        self.addWidget(InfoPad(), "info")
        self.addWidget(HealthPad(
                    charMap.get("healthfull", ("@",7, 2)),
                    charMap.get("healthempty", ("-",7, 1)),
                    self.colours),
            "health")
        self.addWidget(InventoryPad("Inventory"), "inventory")
        self.addWidget(InventoryPad("Ground"), "ground")
        self.addWidget(InventoryPad("Equipment"), "equipment")
        self.addWidget(MessagePad(), "msg")
        self.addWidget(TextInput(), "textinput")
        
        self.lastinfostring = None
        
        self.forced = False
        self.update()
    
    def addWidget(self, pad, name, winname=None):
            if not winname:
                winname = name
            widget = Widget(pad)
            self.widgets[name] = widget
            widget.setWin(winname, self.screen)
    
    def getWidget(self, name):
        if name in self.widgets:
            return self.widgets[name].getImpl()
        else:
            return None
    
    def resizeField(self, size):
        self.getWidget("field").resize(*size)
    
    def drawFieldCells(self, cells):
        field = self.getWidget("field")
        for cell in cells:
            (x, y), spriteNames = cell
            sprites = [self.getChar(spriteName) for spriteName in spriteNames]
            if not len(sprites):
                sprites = [self.getChar(" ")]
            field.changeCell(x, y, sprites)
        
    
    def setFieldCenter(self, pos):
        self.getWidget("field").setCenter(pos)
    
    def setHealth(self, health, maxHealth):
        self.getWidget("health").setHealth(health, maxHealth)
        
    
    def showInfo(self, infostring):
        if infostring != self.lastinfostring:
            self.getWidget("info").showString(infostring)
            
            self.lastinfostring = infostring
    
    def setInventory(self, items):
        self.getWidget("inventory").setInventory(items)
        
    
    def setEquipment(self, slots):
        self.getWidget("equipment").setInventory(
            sorted([
                slot + ": " + (item if item else "")
                for slot, item in slots.items()
            ])
        )
    
    def setGround(self, items):
        self.getWidget("ground").setInventory(items)
    
    def getSelector(self, name):
        widget = self.getWidget(name)
        if not widget or not hasattr(widget, "getSelector"):
            return None
        return widget.getSelector()
        
    
    def addMessage(self, message):
        self.getWidget("msg").addMessage(message)
    
    def getChar(self, sprite):
        """This returns the character belonging to some spritename. This does not read a character"""
        return self.characters.get(sprite, self.defaultChar)
    
    def getString(self):
        """This does actually read input"""
        return str(self.getWidget("textinput").getString(), "utf-8")
    
    def update(self):
        changed = False
        for widget in self.widgets.values():
            if self.forced or widget.isChanged():
                widget.update()
                changed = True
        
        if changed:
            self.screen.update()
        self.forced = False
    
    def forceUpdate(self):
        self.forced = True

