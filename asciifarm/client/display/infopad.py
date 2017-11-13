
import curses



class InfoPad:
    
    
    
    def __init__(self):
        self.changed = False
        self.lines = []
    
    def showString(self, string):
        self.lines = string.split('\n')
        self.changed = True
    
    def update(self, win, force):
        if not self.changed and not force or not win:
            return
        height, width = win.getmaxyx()
        lines = [line[:width-1] for line in self.lines][:height]
        text = '\n'.join(lines)
        win.erase()
        win.addstr(0, 0, text)
        self.changed = False
        win.noutrefresh()
