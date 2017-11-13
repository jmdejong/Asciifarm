
import curses
from .fieldpad import FieldPad

import signal

class Screen:
    
    
    def __init__(self, display, stdscr):
        self.display = display
        curses.curs_set(0)
        self.stdscr = stdscr
        #self.height, self.width = self.stdscr.getmaxyx()
        self.setWins()
        signal.signal(signal.SIGWINCH, self.updateSize)
    
    def _limitHeight(self, h, y):
        return min(h + y, self.height) - y
    
    def setWins(self):
        height, width = self.height, self.width = self.stdscr.getmaxyx()
        
        sideW = 20
        sideX = width-sideW
        msgH = max(3, min(height // 5, 6))
        msgY = height - msgH
        healthY = 0
        healthH = self._limitHeight(2, healthY)
        groundY = healthY + healthH
        groundH = self._limitHeight(7, groundY)
        invY = groundY + groundH
        invH = self._limitHeight(12, invY)
        infoY = invY + invH
        infoH = self._limitHeight(20, infoY)
        
        
        self.fieldWin = curses.newwin(msgY, sideX - 1, 0, 0)
        self.msgWin = curses.newwin(msgH, sideX - 1, msgY, 0)
        self.healthWin = curses.newwin(healthH, sideW, healthY, sideX)
        self.groundWin = curses.newwin(groundH, sideW, groundY, sideX)
        self.inventoryWin = curses.newwin(invH, sideW, invY, sideX)
        self.infoWin = curses.newwin(infoH, sideW, infoY, sideX)
    
    
    
    def updateSize(self, *args):
        curses.endwin()
        curses.initscr()
        self.setWins()
        #self.height, self.width = self.stdscr.getmaxyx()
        self.stdscr.clear()
        self.update(True)
    
    def update(self, force=False):
        d = self.display
        d.fieldPad.update(self.fieldWin, force)
        d.messagePad.update(self.msgWin, force)
        d.healthPad.update(self.healthWin, force)
        d.groundPad.update(self.groundWin, force)
        d.inventoryPad.update(self.inventoryWin, force)
        d.infoPad.update(self.infoWin, force)
    
    def getWidth(self):
        return self.width
    
    def getHeight(self):
        return self.height
    
    #def update(self
