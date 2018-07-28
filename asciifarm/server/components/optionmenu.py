

from .component import Component


class OptionMenu(Component):
    
    def __init__(self, description, options):
        self.description = description
        self.options = {option.name: option for option in options}
    
    def attach(self, obj):
        self.owner = obj
    
    def getOptions(self):
        return list(self.options.values())
    
    def choose(self, option, obj):
        if option in self.options:
            self.options[option].act(obj)



