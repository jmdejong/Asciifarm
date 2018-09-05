


class Widget:
    
    
    def __init__(self, impl):
        self.impl = impl
        self.impl.setWidget(self)
        
        self.win = None
        self.screen = None
        self.changed = False
    
    def setWin(self, win, screen):
        self.win = win
        self.screen = screen
    
    def getWin(self):
        return self.win and self.screen and self.screen.getWin(self.win)
    
    def getImpl(self):
        return self.impl
    
    def change(self):
        self.changed = True
    
    def doUpdate(self):
        self.screen.update()
    
    def isChanged(self):
        return self.changed
    
    def update(self):
        if not self.getWin() or self.getWin().hidden:
            return
        self.impl.update(self.getWin())
        self.changed = False
