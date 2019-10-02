
from random import random as rand
from .dc import DC
from ..template import Template

class Loot(DC):
    
    def __init__(self, items):
        self.items = []
        for item in items:
            if isinstance(item, Template) or isinstance(item, str):
                item = (item, 1)
            assert len(item) == 2, ValueError(item)
            template, chance = item
            if isinstance(template, str):
                template = Template(template)
            self.items.append((template, chance))
    
    def pick(self):
        return [template for template, chance in self.items if chance > rand()]
