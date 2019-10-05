
# todo: make sure growing continues in unloaded rooms

class Periodic:
    
    def __init__(self, components, interval=None, targetTime=None, randomise=False):
        self.interval = interval
        self.components = components
        self.randomise = randomise
        self.targetTime = targetTime
    
