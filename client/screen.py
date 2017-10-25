
import curses
from .fieldpad import FieldPad

import signal

SIDEWIDTH = 15

class Screen:
    
    
    def __init__(self, stdscr, maxSize=(float("inf"),float("inf")), charSize=1):
        curses.curs_set(0)
        self.stdscr = stdscr
        self.updateSize()
        self.changed = False
        signal.signal(signal.SIGWINCH, self.updateSize)
    
    def updateSize(self, *args):
        self.height, self.width = self.stdscr.getmaxyx()
    
    def getWidth(self):
        return self.width
    
    def getHeight(self):
        return self.height
    
    def change(self):
        self.changed = True
    
    def update(self, fieldPad, infoPad):
        if self.changed:
            fieldEnd = min(fieldPad.getWidth()-1, self.getWidth()-SIDEWIDTH-2)
            fieldPad.update(self, 0,0,fieldEnd, min(fieldPad.getHeight(), self.getHeight()-1))
            infoPad.update(self, fieldEnd+2,0, self.getWidth()-1, self.getHeight()-1)
            curses.doupdate()
        self.changed = False
        
