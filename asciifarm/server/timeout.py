


class Timeout:
    """ Helper class for components that have to wait several updates before doing something """
    
    def __init__(self, timeEvent, time=1, callback=None):
        self.time = time
        self.timeEvent = timeEvent
        self.cooldown = time
        self.callback = callback
        self.timeEvent.addListener(self.update)
    
    def isReady(self):
        return self.cooldown <= 0
    
    def timeLeft(self):
        return self.cooldown
    
    def update(self, steps):
        self.cooldown = max(self.cooldown-steps, 0)
        if self.isReady():
            self.remove()
            if self.callback:
                self.callback(self)
                self.callback = None
    
    def remove(self):
        self.timeEvent.removeListener(self.update)
