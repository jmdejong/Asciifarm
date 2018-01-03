
import curses

class HealthPad:
    
    def __init__(self, char=('@',7,0), emptyChar=('-',7,0), colours=False):
        self.char = char
        self.emptyChar = emptyChar
        self.changed = False
        self.colours = colours
        self.health = 0
        self.maxHealth = 0
        self.widget = None
    
    def setWidget(self, widget):
        self.widget = widget
    
    def setHealth(self, health, maxHealth):
        self.health = health
        self.maxHealth = maxHealth
        self.widget.change()
    
    def update(self):
        win = self.widget.getWin()
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
