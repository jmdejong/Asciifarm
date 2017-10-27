
import curses

class HealthPad:
    
    def __init__(self, width=1, char=('@',7,0), emptyChar=('-',7,0), colours=False):
        self.char = char
        self.emptyChar = emptyChar
        self.pad = curses.newpad(2, width+1)
        self.width = width
        self.changed = False
        self.lastView = None
        self.colours = colours
    
    def setHealth(self, health, maxHealth):
        self.pad.erase()
        barEnd = round(health/maxHealth * self.width)
        self.pad.addstr(0,0,"Health: {}/{}".format(health, maxHealth)[:self.width])
        if self.colours:
            self.pad.addstr(1,0, self.char[0]*barEnd, self.colours.get(*self.char[1:]))
            self.pad.addstr(1,barEnd, self.emptyChar[0]*(self.width-barEnd), self.colours.get(*self.emptyChar[1:]))
        else:
            self.pad.addstr(1,0, self.char[0]*barEnd)
            self.pad.addstr(1,barEnd, self.emptyChar[0]*(self.width-barEnd))
            
        self.changed = True
    
    def getHeight(self):
        return 2
    
    def update(self, screen, x, y, xmax, ymax):
        if not self.changed and (x, y, xmax, ymax) == self.lastView:
            return
        self.lastView = (x, y, xmax, ymax)
        self.changed = False
        self.pad.noutrefresh(
            0,
            0,
            y,
            x,
            ymax-1,
            xmax-1)
