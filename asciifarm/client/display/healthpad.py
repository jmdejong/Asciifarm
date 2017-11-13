
import curses

class HealthPad:
    
    def __init__(self, width=1, char=('@',7,0), emptyChar=('-',7,0), colours=False):
        self.char = char
        self.emptyChar = emptyChar
        #self.pad = curses.newpad(2, width+1)
        #self.width = width
        self.changed = False
        #self.lastView = None
        self.colours = colours
        self.health = 0
        self.maxHealth = 0
    
    def setHealth(self, health, maxHealth):
        self.health = health
        self.maxHealth = maxHealth
        
        
        #self.pad.erase()
        #barEnd = round(health/maxHealth * self.width)
        #self.pad.addstr(0,0,"Health: {}/{}".format(health, maxHealth)[:self.width])
        #if self.colours:
            #self.pad.addstr(1,0, self.char[0]*barEnd, self.colours.get(*self.char[1:]))
            #self.pad.addstr(1,barEnd, self.emptyChar[0]*(self.width-barEnd), self.colours.get(*self.emptyChar[1:]))
        #else:
            #self.pad.addstr(1,0, self.char[0]*barEnd)
            #self.pad.addstr(1,barEnd, self.emptyChar[0]*(self.width-barEnd))
            
        self.changed = True
    
    #def getHeight(self):
        #return 2
    
    def update(self, win, force=False):
        if not self.changed and not force or not win:
            return
        #self.lastView = (x, y, xmax, ymax)
        self.changed = False
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
            #0,
            #0,
            #y,
            #x,
            #ymax-1,
            #xmax-1)
