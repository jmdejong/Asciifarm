
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
        height, width = win.getmaxyx()
        width -= 1
        barEnd = round(self.health/self.maxHealth * width) if self.maxHealth > 0 else 0
        win.erase()
        win.addstr(0,0,"Health: {}/{}".format(self.health, self.maxHealth)[:width])
        if self.colours:
            win.addstr(1,0, self.char[0]*barEnd, self.colours.get(*self.char[1:]))
            win.addstr(1,barEnd, self.emptyChar[0]*(width-barEnd), self.colours.get(*self.emptyChar[1:]))
        else:
            win.addstr(1,0, self.char[0]*barEnd)
            win.addstr(1,barEnd, self.emptyChar[0]*(width-barEnd))
        win.noutrefresh()
