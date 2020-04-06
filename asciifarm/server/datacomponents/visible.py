

class Visible:
    
    def __init__(self, sprite=" ", height=0, name=None):
        self.sprite = sprite
        self.height = height
        if name is None:
            name = sprite
        self.name = name
            
