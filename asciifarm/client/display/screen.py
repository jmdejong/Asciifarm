
import curses
from .fieldpad import FieldPad

import signal


class Screen:
    
    
    def __init__(self, stdscr, maxSize=(float("inf"),float("inf")), charSize=1):
        curses.curs_set(0)
        self.stdscr = stdscr
        self.height, self.width = self.stdscr.getmaxyx()
        signal.signal(signal.SIGWINCH, self.updateSize)
    
    def updateSize(self, *args):
        curses.endwin()
        curses.initscr()
        self.height, self.width = self.stdscr.getmaxyx()
        self.stdscr.clear()
    
    def getWidth(self):
        return self.width
    
    def getHeight(self):
        return self.height
        
