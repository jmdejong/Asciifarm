

from .listselector import ListSelector

class SwitchSelector(ListSelector):
    
    
    
    def setItems(self, items):
        super().setItems(items)
        self.updateVisibility()
    
    def updateVisibility(self):
        pass
        #for i, (_menu, widget, _title) in enumerate(self.items):
            #if i == self.selector:
                #widget.hidden = False
                #widget.change()
            #else:
                #widget.hidden = True
    
    def doSelect(self, value):
        
        #self.getSelectedItem().widget.hidden = True
        super().doSelect(value)
        self.updateVisibility()
        #self.getSelectedItem().widimp.change()
        #newWid.hidden = False
        #newWid.change()
    
    def itemName(self, item):
        _menu, _widget, title = item
        return title
