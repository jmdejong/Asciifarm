
import curses



class InfoPad:
    
    
    
    def __init__(self):
        self.changed = False
        self.lines = []
        self.win = None
    
    def setWin(self, win):
        self.win = win
    
    def showString(self, string):
        self.lines = string.split('\n')
        self.changed = True
    
    def update(self, force):
        if not self.changed and not force or not self.win:
            return
        win = self.win
        height, width = win.getmaxyx()
        lines = [line[:width-1] for line in self.lines][:height]
        text = '\n'.join(lines)
        win.erase()
        win.addstr(0, 0, text)
        self.changed = False
        win.noutrefresh()
