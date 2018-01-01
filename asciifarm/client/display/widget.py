


class Widget:
    
    
    def __init__(self, impl):
        self.impl = impl
        self.impl.setWidget(self)
        
        self.win = None
        self.changed = False
    
    def setWin(self, win):
        self.win = win
    
    def getWin(self):
        return self.win
    
    def getImpl(self):
        return self.impl
    
    def change(self):
        self.changed = True
    
    def update(self):
        if not self.changed or not self.win:
            return
        self.impl.update()
        self.changed = False
