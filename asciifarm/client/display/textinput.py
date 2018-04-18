
import curses

class TextInput:
    
    def __init__(self):
        self.widget = None
        self.text = ""
        self.cursor = 0
    
    def setWidget(self, widget):
        self.widget = widget
    
    def setText(self, text, cursor):
        self.text = text
        self.cursor = cursor
        self.widget.change()
    
    def update(self):
        win = self.widget.getWin()
        width, height = win.getSize()
        win.erase()
        win.addLine((0, 0), self.text)
        if self.cursor >= 0 and self.cursor <= len(self.text):
            win.setAttr((self.cursor, 0), curses.A_REVERSE)
        win.noutrefresh()
