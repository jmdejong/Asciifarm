


class Timeout:
    
    def __init__(self, timeEvent, time=1):
        self.time = time
        self.timeEvent = timeEvent
        self.cooldown = 0
    
    def isReady(self):
        return self.cooldown <= 0
    
    def timeout(self, time=None):
        if time == None:
            time = self.time
        self.cooldown = time
        self.timeEvent.addListener(self.update)
    
    def update(self, steps):
        self.cooldown = max(self.cooldown-steps, 0)
        if self.isReady():
            self.timeEvent.removeListener(self.update)
    
    def remove(self):
        self.timeEvent.removeListener(self.update)
