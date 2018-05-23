
import curses
from asciifarm.common.utils import clamp
from .window import Window

import signal

class Screen:
    
    def __init__(self, display, stdscr, colours):
        self.display = display
        try:
            curses.curs_set(0)
            self.cursorSet = False
        except curses.error:
            # Not all terminals support this functionality.
            # When the error is ignored the screen will look a little uglier,
            # A cursor will move around, but that's not terrible
            # So in order to keep the game as accesible as possible to everyone, it should be safe to ignore the error.
            self.cursorSet = True
            # It is probably possible to make sure the cursor is only in a corner of the screen
            # but I can't figure out how.
            # it seems to ignore all my move commands unless I press a key
            # I give up
        self.stdscr = stdscr
        self.colours = colours
        self.setWins()
        signal.signal(signal.SIGWINCH, self.updateSize)
    
    def _limitHeight(self, h, y):
        return min(h + y, self.height) - y
    
    def setWins(self):
        height, width = self.height, self.width = self.stdscr.getmaxyx()
        
        sideW = 20
        sideX = width-sideW
        msgH = clamp(height // 5, 3, 5)
        msgY = height - msgH-1
        inputH = 1
        inputY = msgY + msgH
        healthY = 0
        healthH = self._limitHeight(2, healthY)
        groundY = healthY + healthH
        groundH = self._limitHeight(6, groundY)
        invY = groundY + groundH
        invH = self._limitHeight(9, invY)
        eqY = invY + invH
        eqH = self._limitHeight(5, eqY)
        infoY = eqY + eqH
        infoH = self._limitHeight(20, infoY)
        
        self.windows = {
            "field": self.makeWin(0, 0, sideX - 1, msgY),
            "msg": self.makeWin(0, msgY, sideX - 1, msgH),
            "textinput": self.makeWin(0, inputY, sideX - 1, inputH),
            "health": self.makeWin(sideX, healthY, sideW, healthH),
            "ground": self.makeWin(sideX, groundY, sideW, groundH),
            "inventory": self.makeWin(sideX, invY, sideW, invH),
            "equipment": self.makeWin(sideX, eqY, sideW, eqH),
            "info": self.makeWin(sideX, infoY, sideW, infoH)
        }
    
    def makeWin(self, x, y, width, height):
        if width < 1 or height < 1:
            win = None
        else:
            win = curses.newwin(height, width, y, x)
        return Window(win, self.colours)
    
    def getWin(self, name):
        return self.windows.get(name, None)
    
    def updateSize(self, *args):
        curses.endwin()
        curses.initscr()
        self.setWins()
        self.stdscr.clear()
        self.display.forceUpdate()
    
    def update(self):
        curses.doupdate()
    
    def getWidth(self):
        return self.width
    
    def getHeight(self):
        return self.height
    
    
