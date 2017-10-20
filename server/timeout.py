


class Timeout:
    
    def __init__(self, timeEvent, time=1, callback=None):
        self.time = time
        self.timeEvent = timeEvent
        self.cooldown = 0
        self.defaultCallback = callback
    
    def isReady(self):
        return self.cooldown <= 0
    
    def timeout(self, time=None, callback=None):
        if time == None:
            time = self.time
        self.callback = callback or self.defaultCallback
        self.cooldown = time
        self.timeEvent.addListener(self.update)
    
    def update(self, steps):
        self.cooldown = max(self.cooldown-steps, 0)
        if self.isReady():
            self.timeEvent.removeListener(self.update)
            if self.callback:
                self.callback()
                self.callback = None
    
    def remove(self):
        self.timeEvent.removeListener(self.update)
