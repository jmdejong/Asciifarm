


import os
from ratuil.layout import Layout
from ratuil.bufferedscreen import BufferedScreen as Screen
#from ratuil.screen import Screen
from ratuil.textstyle import TextStyle
from asciifarm.common.utils import get
from .listselector import ListSelector


SIDEWIDTH = 20

ALPHABET = "!\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~"

class Display:
    
    def __init__(self, charMap):
        
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
        
        self.messageColours = charMap.get("msgcolours", {})
        
        fname = os.path.join(os.path.dirname(__file__), "layout.xml")
        with open(fname) as f:
            layouttext = f.read()
        
        self.layout = Layout(layouttext)
        self.layout.get("field").set_char_size(charMap.get("charwidth", 1))
        
        self.screen = Screen()
        self.screen.clear()
        
        self.layout.set_target(self.screen)
        self.layout.update()
        
        
        
        # temporary, until these have a better place
        self.inventory = ListSelector(self.getWidget("inventory"))
        self.equipment = ListSelector(self.getWidget("equipment"))
        self.ground = ListSelector(self.getWidget("ground"))
        self.switch = ListSelector(self.getWidget("switchtitles"))
        
        self.switch.setItems(["inventory", "equipment", "ground"])
        self.menus = {
            "inventory": self.inventory,
            "equipment": self.equipment,
            "ground": self.ground
        }
        
        self.layout.get("switch").select(0)
        
    
    def getWidget(self, name):
        return self.layout.get(name)
    
    def resizeField(self, size):
        self.getWidget("field").set_size(*size)
    
    def drawFieldCells(self, cells):
        field = self.getWidget("field")
        for cell in cells:
            (x, y), spriteNames = cell
            if not len(spriteNames):
                char, fg, bg = self.getChar(' ')
            else:
                char, fg, bg = self.getChar(spriteNames[0])
                for spriteName in spriteNames[1:]:
                    if bg is not None:
                        break
                    _char, _fg, bg = self.getChar(spriteName)
            field.change_cell(x, y, char, TextStyle(fg, bg))
        
    
    def setFieldCenter(self, pos):
        self.getWidget("field").set_center(*pos)
    
    def setHealth(self, health, maxHealth):
        if health is None:
            health = 0
        if maxHealth is None:
            maxHealth = 0
        self.getWidget("health").set_total(maxHealth)
        self.getWidget("health").set_filled(health)
        
    
    def showInfo(self, infostring):
        self.getWidget("info").set_text(infostring)
            
    def selectMenu(self, *args, **kwargs):
        self.switch.select(*args, **kwargs)
        self.layout.get("switch").select(self.getSelectedMenu())
    
    def getSelectedMenu(self):
        return self.switch.getSelectedItem()
    
    def getSelectedItem(self, menu=None):
        return self._getMenu(menu).getSelected()
    
    def selectItem(self, menu=None, *args, **kwargs):
        self._getMenu(menu).select(*args, **kwargs)
    
    def _getMenu(self, name=None):
        if name is None:
            name = self.getSelectedMenu()
        name = name.casefold()
        return self.menus[name]
    
    def setInventory(self, items):
        self.getWidget("inventory").set_items(items)
        
    
    def setEquipment(self, slots):
        self.getWidget("equipment").set_items(
            sorted([
                slot + ": " + (item if item else "")
                for slot, item in slots.items()
            ])
        )
    
    def setGround(self, items):
        self.getWidget("ground").set_items(items)
        
    
    def addMessage(self, message, type):
        self.getWidget("msg").add_message(message, TextStyle(*self.messageColours.get(type, (7,0))))
    
    def scrollBack(self, amount, relative=True):
        self.getWidget("msg").scroll(amount, relative)
    
    def setInputString(self, string, cursor):
        self.getWidget("textinput").set_text(string, cursor)
    
    def update(self):
        self.layout.update()
        self.screen.update()
    
    def getChar(self, sprite):
        """This returns the character belonging to some spritename. This does not read a character"""
        return self.characters.get(sprite, self.defaultChar)
    
    def update_size(self):
        self.screen.reset()

