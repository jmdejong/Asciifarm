
import curses



class InfoPad:
    
    
    
    def __init__(self):
        self.changed = False
        self.lines = []
        self.widget = None
    
    def setWidget(self, widget):
        self.widget = widget
    
    def showString(self, string):
        self.lines = string.split('\n')
        self.widget.change()
    
    def update(self):
        win = self.widget.getWin()
        width, height = win.getSize()
        lines = [line[:width-1] for line in self.lines][:height]
        text = '\n'.join(lines)
        win.erase()
        win.addLine((0, 0), text)
        win.noutrefresh()
