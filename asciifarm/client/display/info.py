

class Info:
    
    def __init__(self):
        self.changed = False
        self.lines = []
        self.widget = None
        self.lastString = None
    
    def setWidget(self, widget):
        self.widget = widget
    
    def showString(self, string):
        if string == self.lastString:
            return
        self.lines = string.split('\n')
        self.widget.change()
        self.lastString = string
    
    def update(self):
        win = self.widget.getWin()
        width, height = win.getSize()
        lines = [line[:width-1] for line in self.lines][:height]
        win.erase()
        for i, line in enumerate(lines):
            win.addLine((0, i), line)
        win.noutrefresh()
