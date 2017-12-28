
import curses

class TextInput:
    
    def __init__(self):
        self.reading = False
        self.win = None
    
    def setWin(self, win):
        self.win = win
    
    def getString(self):
        if not self.win:
            return None
        self.reading = True
        curses.echo()
        curses.nocbreak()
        self.win.addstr(0, 0, ">")
        string = self.win.getstr(0,2)
        curses.noecho()
        curses.cbreak()
        self.reading = False
        self.win.erase()
        self.win.noutrefresh()
        return string
    
    def update(self, force=False):
        pass
