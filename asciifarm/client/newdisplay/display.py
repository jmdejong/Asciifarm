


import os
from ratuil.layout import Layout
from ratuil.bufferedscreen import BufferedScreen as Screen
#from ratuil.screen import Screen
from ratuil.textstyle import TextStyle
from asciifarm.common.utils import get


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
        
        
        #screen = Screen(self, stdscr, self.colours)
        #self.screen = screen
        
        #self.widgets = {}
        
        #self.addWidget(Field((1, 1), charMap.get("charwidth", 1), self.colours), "field")
        #self.addWidget(Info(), "info")
        #self.addWidget(Health(
                    #charMap.get("healthfull", ("@",7, 2)),
                    #charMap.get("healthempty", ("-",7, 1))
                #),
            #"health")
        #self.addWidget(Inventory("Inventory"), "inventory")
        #self.addWidget(Inventory("Ground"), "ground")
        #self.addWidget(Inventory("Equipment"), "equipment")
        
        
        ##switcher = Switcher([self.widgets["ground"], self.widgets["inventory"], self.widgets["equipment"]], 1)
        #self.addWidget(Inventory(""), "switch")
        #self.addWidget(Messages(charMap.get("msgcolours", {})), "msg")
        #self.addWidget(TextInput(), "textinput")
        
        #self.forced = False
    
    #def addWidget(self, w, name, winname=None):
        #if not winname:
            #winname = name
        #widget = Widget(w, name)
        #self.widgets[name] = widget
        #widget.setWin(winname, self.screen)
    
    def getWidget(self, name):
        return self.layout.get(name)
        #if name in self.widgets:
            #return self.widgets[name].getImpl()
        #else:
            #return None
    
    def resizeField(self, size):
        self.getWidget("field").set_size(*size)
        #self.forced = True
    
    def drawFieldCells(self, cells):
        field = self.getWidget("field")
        for cell in cells:
            (x, y), spriteNames = cell
            if not len(spriteNames):
                char, fg, bg = self.getChar(0)
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
        self.getWidget("health").set_total(maxHealth)
        self.getWidget("health").set_filled(health)
        
    
    def showInfo(self, infostring):
        pass
        #self.getWidget("info").showString(infostring)
            
    
    #def setInventory(self, items):
        #self.getWidget("inventory").setInventory(items)
        
    
    #def setEquipment(self, slots):
        #self.getWidget("equipment").setInventory(
            #sorted([
                #slot + ": " + (item if item else "")
                #for slot, item in slots.items()
            #])
        #)
    
    #def setGround(self, items):
        #self.getWidget("ground").setInventory(items)
        
    
    def addMessage(self, message, type):
        self.getWidget("msg").add_message(message, TextStyle(*self.messageColours.get(type, (7,0))))
    
    def scrollBack(self, amount, relative=True):
        self.getWidget("msg").scroll(amount, relative)
    
    def setInputString(self, string, cursor):
        self.getWidget("textinput").set_text(string, cursor)
    
    def update(self):
        self.layout.update()
        self.screen.update()
        #changed = False
        #for widget in self.widgets.values():
            #if self.forced or widget.isChanged():
                #widget.update()
                #changed = True
        #if changed:
            #self.screen.update()
        #self.forced = False
    
    #def forceUpdate(self):
        #self.forced = True
    
    def getChar(self, sprite):
        """This returns the character belonging to some spritename. This does not read a character"""
        return self.characters.get(sprite, self.defaultChar)
    
    def update_size(self):
        self.screen.reset()

