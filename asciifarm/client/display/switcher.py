

from .inventory import Inventory

class Switcher(Inventory):
    """An area that can contain multiple widgets but only shows one at a time.
    There is a function to switch between the displayed widgets.
    """
    
    def __init__(self, widgets, initial=0):
        Inventory.__init__(self, "", "")
        self.setInventory(widgets)
        
        for wid in widgets:
            wid.hidden = True
        
        self.select(initial)
    
    def doSelect(self, value):
        self.getSelectedItem().hidden = True
        self.selector = value
        self.change()
        newWid = self.getSelectedItem()
        newWid.hidden = False
        newWid.change()
    
    def itemName(self, item):
        return item.getImpl().title

