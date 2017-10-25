
import curses

class Screen:
    
    
    def __init__(self, stdscr):
        curses.curs_set(0)
        self.height, self.width = stdscr.getmaxyx()
        self.stdscr = stdscr
        self.fieldpad = curses.newpad(100,200)
        self.infopad = curses.newpad(100,100)
        self.healthpad = curses.newpad(2, 100)
        self.changed = False
    
    def changeCells(self, cells, width, height):
        for x, y, char in cells:
            self.fieldpad.addstr(y, x, char)
        self.height, self.width = self.stdscr.getmaxyx()
        self.fieldpad.noutrefresh(0,0,0,0,min(height, self.height-1), min(width, self.width-1))
        self.changed = True
    
    def putPlayers(self, players, x=0, y=0):
        self.infopad.clear()
        self.infopad.addstr(0, 0, players)
        self.height, self.width = self.stdscr.getmaxyx()
        #print(x, y, self.width, self.height)
        if x < self.width and y < self.height:
            self.infopad.noutrefresh(0,0,y,x,self.height-1,self.width-1)
            self.changed = True
    
    #def showHealth(self, health, maxHealth):
        #self.healthpad.addStr(0,0, "Health: ({}/{})".format(health, maxHealth
    
    def refresh(self):
        if self.changed:
            curses.doupdate()
        self.changed = False
