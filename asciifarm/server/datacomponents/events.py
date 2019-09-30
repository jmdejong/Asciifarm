
import collections

class Events:
    
    def __init__(self):
        self.messages = collections.deque()
    
    def add(self, message):
        self.messages.append(message)
