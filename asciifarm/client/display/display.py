

from .field import Field
from .info import Info
from .health import Health
from .inventory import Inventory
from .screen import Screen
from .colours import Colours
from .messages import Messages
from .textinput import TextInput
from .widget import Widget

from asciifarm.common.utils import get


SIDEWIDTH = 20

ALPHABET = "!\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~"

class Display:
    
    def __init__(self, stdscr, charMap, colours=False):
        
        if colours:
            self.colours = Colours()
        else:
            self.colours = None
        self.characters = {}
        
        def parseSprite(sprite):
            if isinstance(sprite, str):
                return (sprite, None, None)
            char = get(sprite, 0, " ")
            fg = get(sprite, 1)
            bg = get(sprite, 2)
            return (char, fg, bg)
        for name, sprite in charMap["mapping"].items():
            vals = parseSprite(sprite)
            if vals:
                self.characters[name] = vals
        
        for name, colours in charMap.get("writable", {}).items():
            fg = get(colours, 0)
            bg = get(colours, 1)
            for i in range(min(len(ALPHABET), len(charMap.get("alphabet", [])))):
                self.characters[name + '-' + ALPHABET[i]] = (charMap["alphabet"][i], fg, bg)
        
        self.defaultChar = parseSprite(charMap.get("default", "?"))
        self.screen = Screen(self, stdscr, self.colours)
        
        self.widgets = {}
        
        self.addWidget(Field((1, 1), charMap.get("charwidth", 1), self.colours), "field")
        self.addWidget(Info(), "info")
        self.addWidget(Health(
                    charMap.get("healthfull", ("@",7, 2)),
                    charMap.get("healthempty", ("-",7, 1)),
                    self.colours),
            "health")
        self.addWidget(Inventory("Inventory"), "inventory")
        self.addWidget(Inventory("Ground"), "ground")
        self.addWidget(Inventory("Equipment"), "equipment")
        self.addWidget(Messages(), "msg")
        self.addWidget(TextInput(), "textinput")
        
        self.lastinfostring = None
        
        self.forced = False
        self.update()
    
    def addWidget(self, w, name, winname=None):
            if not winname:
                winname = name
            widget = Widget(w)
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
        
    
    def addMessage(self, message):
        self.getWidget("msg").addMessage(message)
    
    def scrollBack(self, amount, relative=True):
        self.getWidget("msg").scroll(amount, relative)
    
    def getChar(self, sprite):
        """This returns the character belonging to some spritename. This does not read a character"""
        return self.characters.get(sprite, self.defaultChar)
    
    def setInputString(self, string, cursor):
        self.getWidget("textinput").setText(string, cursor)
    
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

