


class Exchange:
    
    def __init__(self, products, costs, description=None, name=None):
        self.products = products
        self.costs = costs
        if description is None:
            description = "{} ({})".format(", ".join(str(p) for p in products), ", ".join(str(c) for c in costs))
        self.description = description
        self.name = name or id(self)

class Exchanger:
    
    def __init__(self, options, description=""):
        self.options = {option.name: option for option in options}
        self.description = description
        
