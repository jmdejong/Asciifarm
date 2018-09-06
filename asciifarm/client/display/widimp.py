

class WidImp:
    
    """widget implementation"""
    
    _widget = None
    
    def setWidget(self, widget):
        self._widget = widget
        self.change()
    
    def change(self):
        if self._widget is not None:
            self._widget.change()
    
    def update(self, win):
        pass
