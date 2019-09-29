

class AI:
    
    def __init__(self, viewDist=0, moveChance=1, home=None, homesickness=0.05):
        self.moveChance = moveChance
        self.viewDist = viewDist
        self.home = home # Should home be a place instead of object? that would reduce references. A: Yes
        self.homesickness = homesickness
