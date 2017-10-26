
import curses
from .fieldpad import FieldPad

import signal

SIDEWIDTH = 15
HEALTHHEIGHT = 1

class Screen:
    
    
    def __init__(self, stdscr, maxSize=(float("inf"),float("inf")), charSize=1):
        curses.curs_set(0)
        self.stdscr = stdscr
        self.height, self.width = self.stdscr.getmaxyx()
        self.changed = False
        signal.signal(signal.SIGWINCH, self.updateSize)
    
    def updateSize(self, *args):
        curses.endwin()
        curses.initscr()
        self.height, self.width = self.stdscr.getmaxyx()
        self.stdscr.clear()
        self.change()
    
    def getWidth(self):
        return self.width
    
    def getHeight(self):
        return self.height
    
    def change(self):
        self.changed = True
    
    def update(self, fieldPad, infoPad, healthPad):
        if self.changed:
            fieldEnd = min(fieldPad.getWidth(), self.getWidth()-SIDEWIDTH-1)
            fieldPad.update(self, 0,0,fieldEnd, min(fieldPad.getHeight(), self.getHeight()))
            healthPad.update(self, fieldEnd+1,0, self.getWidth(), HEALTHHEIGHT)
            infoPad.update(self, fieldEnd+1,HEALTHHEIGHT, self.getWidth(), self.getHeight())
            curses.doupdate()
        self.changed = False
        
