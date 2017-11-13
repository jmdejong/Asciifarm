
import curses



class InfoPad:
    
    
    
    def __init__(self, size=(1,1), *args):
        #self.pad = curses.newpad(size[1], size[0])
        #self.size = size
        self.changed = False
        self.lines = []
        #self.lastView = None
    
    def showString(self, string):
        self.lines = string.split('\n')
        #self.pad.clear()
        #self.pad.addstr(0,0,string)
        self.changed = True
    
    def update(self, win, force=False):
        if not self.changed and not force or not win:
            return
        #self.lastView = (x, y, xmax, ymax)
        height, width = win.getmaxyx()
        lines = [line[:width] for line in self.lines][:height]
        text = '\n'.join(lines)
        win.erase()
        win.addstr(0, 0, text)
        self.changed = False
        win.noutrefresh()
            #0,
            #0,
            #y,
            #x,
            #ymax-1,
            #xmax-1)
