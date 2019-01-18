

from .widimp import WidImp

class Health(WidImp):
    
    def __init__(self, char=None, emptyChar=None, colours=False):
        self.char = char or ('@',7,0)
        self.emptyChar = emptyChar or ('-',7,0)
        self.changed = False
        self.colours = colours
        self.health = 0
        self.maxHealth = 0
    
    def setHealth(self, health, maxHealth):
        self.health = health or 0
        self.maxHealth = maxHealth or 0
        self.change()
    
    def update(self, win):
        width, height = win.getSize()
        width -= 1
        barEnd = round(self.health/self.maxHealth * width) if self.maxHealth > 0 else 0
        win.erase()
        win.addLine((0,0),"Health: {}/{}".format(self.health, self.maxHealth)[:width])
        if self.colours:
            win.addLine((0, 1), self.char[0]*barEnd, self.char[1:])
            win.addLine((barEnd, 1), self.emptyChar[0]*(width-barEnd), self.emptyChar[1:])
        else:
            win.addLine((0, 1), self.char[0]*barEnd)
            win.addLine((barEnd, 1), self.emptyChar[0]*(width-barEnd))
        win.noutrefresh()
